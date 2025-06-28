# src/expdespy/models/fatorial_base.py

from abc import ABC, abstractmethod
from typing import Dict
from expdespy.models.base import ExperimentalDesign
import scipy.stats as stats
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

from expdespy.posthoc import PostHocLoader


class FatorialDesign(ExperimentalDesign, ABC):
    """
    Classe base para experimentos fatoriais com 2 ou mais fatores.
    Deve ser combinada com delineamentos específicos (DIC, DBC, DQL).
    """

    def __init__(self, data, response, factors):
        self.factors = factors  # lista de strings com os nomes dos fatores
        treatment_formula = "*".join(factors)
        super().__init__(data, response, treatment_formula)

    @abstractmethod
    def _get_formula(self):
        return f"{self.response} ~ {self.treatment}"
    
    def check_assumptions(self, alpha: float = 0.05, print_conclusions: bool = True) -> Dict[str, bool]:
        """
        Verifica os pressupostos da ANOVA para delineamentos fatoriais:
        - Normalidade dos resíduos (Shapiro-Wilk)
        - Homocedasticidade entre combinações fatoriais (Levene)

        Args:
            alpha (float): Nível de significância. Padrão é 0.05.
            print_conclusions (bool): Se True, imprime as conclusões no terminal.

        Returns:
            Dict[str, bool]: Dicionário com os resultados dos testes.
        """
        formula = self._get_formula()
        model = smf.ols(formula, data=self.data).fit()
        residuals = model.resid

        # Teste de normalidade dos resíduos
        normality_p = stats.shapiro(residuals).pvalue
        is_normal = normality_p > alpha

        # Teste de homogeneidade das variâncias entre os grupos fatoriais
        groups = [
            group[self.response].values
            for _, group in self.data.groupby(self.factors)
        ]
        levene_p = stats.levene(*groups).pvalue
        is_homoscedastic = levene_p > alpha

        if print_conclusions:
            print(f"""
    Presupposition Check for Factorial Design:
    1. Normality of Residuals (Shapiro-Wilk)
        - H0: Residuals are normally distributed
        - p-value: {normality_p:.4f}
        - Conclusion: H0 {'not rejected' if is_normal else 'rejected'}

    2. Homoscedasticity (Levene)
        - H0: Variances across factor combinations are equal
        - p-value: {levene_p:.4f}
        - Conclusion: H0 {'not rejected' if is_homoscedastic else 'rejected'}
            """)

        return {
            "normality (Shapiro-Wilk)": {
                "H0": "Residuals are normally distributed",
                "H1": "Residuals are not normally distributed",
                "p-value": normality_p,
                "Conclusion": "H0 must not be rejected" if is_normal else "H0 must be rejected",
            },
            "homoscedasticity (Levene)": {
                "H0": "Variances across groups are equal",
                "H1": "Variances across groups are not equal",
                "p-value": levene_p,
                "Conclusion": "H0 must not be rejected" if is_homoscedastic else "H0 must be rejected",
            }
        }

    def desdobrar_interacao(
        self,
        alpha: float = 0.05,
        print_results: bool = True,
        posthoc: str = "tukey"
    ) -> Dict[str, dict]:
        """
        Desdobra a interação entre os fatores ou aplica testes post hoc nos efeitos principais.

        Args:
            alpha (float): Nível de significância para considerar a interação significativa.
            print_results (bool): Se True, imprime os resultados.
            posthoc (str): Nome do teste post hoc a ser utilizado. Ex: "tukey", "ttest".

        Returns:
            dict: Estrutura com os resultados da ANOVA, testes post hoc e desdobramentos.
        """
        formula = self._get_formula()
        model = smf.ols(formula, data=self.data).fit()
        anova_table = anova_lm(model, typ=2)

        interacao = ":".join([f"C({f})" for f in self.factors])
        estrutura_final = {
            "anova": anova_table,
            "posthoc": {},
            "sub_anova": {},
            "sub_posthoc": {},
        }

        if interacao not in anova_table.index:
            raise ValueError(f"Interação {interacao} não encontrada na ANOVA.")

        p_val = anova_table.loc[interacao, "PR(>F)"]

        if p_val > alpha:
            if print_results:
                print("Interação não significativa. Avaliando efeitos principais com teste post hoc.")
            for fator in self.factors:
                try:
                    test = PostHocLoader.create(
                        test_name=posthoc,
                        data=self.data,
                        values_column=self.response,
                        trats_column=fator,
                        alpha=alpha
                    )
                    resultado = test.run_compact_letters_display()
                    estrutura_final["posthoc"][fator] = resultado
                    if print_results:
                        print(f"\nPost hoc ({posthoc}) para {fator}")
                        print(resultado)
                except Exception as e:
                    if print_results:
                        print(f"Erro ao aplicar post hoc ({posthoc}) em {fator}: {e}")

        else:
            if print_results:
                print("Interação significativa. Realizando desdobramento simples.")
            for f1 in self.factors:
                f2_list = [f for f in self.factors if f != f1]
                for f2 in f2_list:
                    for nivel in sorted(self.data[f2].unique()):
                        subset = self.data[self.data[f2] == nivel]
                        if subset[f1].nunique() <= 1:
                            continue
                        try:
                            model_sub = smf.ols(f"{self.response} ~ C({f1})", data=subset).fit()
                            anova_sub = anova_lm(model_sub, typ=2)
                            chave_anova = f"{f1} dentro de {f2}={nivel}"
                            estrutura_final["sub_anova"][chave_anova] = anova_sub
                            if print_results:
                                print(f"\nAnálise de {chave_anova}")
                                print(anova_sub)

                            test_posthoc = PostHocLoader.create(
                                test_name=posthoc,
                                data=subset,
                                values_column=self.response,
                                trats_column=f1,
                                alpha=alpha
                            )
                            resultado_posthoc = test_posthoc.run_compact_letters_display()
                            estrutura_final["sub_posthoc"][chave_anova] = resultado_posthoc
                            if print_results:
                                print(resultado_posthoc)
                        except Exception as e:
                            if print_results:
                                print(f"Erro ao analisar {f1} dentro de {f2}={nivel}: {e}")

        return estrutura_final
