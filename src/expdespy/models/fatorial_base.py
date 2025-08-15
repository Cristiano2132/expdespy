from abc import ABC, abstractmethod
from typing import Dict, List, Union
from itertools import combinations
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from tabulate import tabulate
from expdespy.models.base import ExperimentalDesign
from expdespy.posthoc import PostHocLoader


class FatorialDesign(ExperimentalDesign, ABC):
    def __init__(self, data, response: str, factors: List[str]):
        self.original_factors = factors
        self.data = data.copy()
        self.factors = [self._safe_factor(f) for f in factors]
        treatment_formula = "*".join([f"C({f})" for f in self.factors])
        super().__init__(self.data, response, treatment_formula)

    def _safe_factor(self, factor_name: str) -> str:
        """
        Garante que o nome do fator não entra em conflito com a sintaxe da fórmula do Patsy/statsmodels.
        Renomeia 'C' para 'C_' e outros nomes problemáticos.
        """
        reserved_names = {"C"}  # Adicione mais nomes aqui se necessário

        if factor_name in reserved_names and factor_name in self.data.columns:
            new_name = factor_name + "_"
            self.data.rename(columns={factor_name: new_name}, inplace=True)
            return new_name

        return factor_name

    @abstractmethod
    def _get_formula(self) -> str:
        pass

    def check_assumptions(
        self, alpha: float = 0.05, print_conclusions: bool = True
    ) -> Dict[str, bool]:
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

        normality_p = stats.shapiro(residuals).pvalue
        is_normal = normality_p > alpha

        groups = [
            group[self.response].values for _, group in self.data.groupby(self.factors)
        ]
        levene_p = stats.levene(*groups).pvalue
        is_homoscedastic = levene_p > alpha

        if print_conclusions:
            print(
                f"""
    Verificação de pressupostos para delineamento fatorial:
    1. Normalidade dos resíduos (Shapiro-Wilk)
        - H0: Resíduos são normalmente distribuídos
        - p-valor: {normality_p:.4f}
        - Conclusão: H0 {'não rejeitada' if is_normal else 'rejeitada'}

    2. Homocedasticidade (Levene)
        - H0: As variâncias são homogêneas entre os grupos
        - p-valor: {levene_p:.4f}
        - Conclusão: H0 {'não rejeitada' if is_homoscedastic else 'rejeitada'}
            """
            )

        return {
            "normality (Shapiro-Wilk)": {
                "H0": "Resíduos são normalmente distribuídos",
                "H1": "Resíduos não são normalmente distribuídos",
                "p-value": normality_p,
                "Conclusion": "H0 não rejeitada" if is_normal else "H0 rejeitada",
            },
            "homoscedasticity (Levene)": {
                "H0": "As variâncias entre grupos são iguais",
                "H1": "As variâncias entre grupos são diferentes",
                "p-value": levene_p,
                "Conclusion": (
                    "H0 não rejeitada" if is_homoscedastic else "H0 rejeitada"
                ),
            },
        }

    def run_anova(self, max_interaction: int = None) -> pd.DataFrame:
        """
        Executa a ANOVA incluindo apenas interações até um certo nível
        e adiciona marcadores de significância (*, **, ***, ns).

        Args:
            max_interaction (int, opcional): Nível máximo de interação a incluir (1 = principais, 2 = duplas, ...).
                                            Se None, usa todas as interações possíveis.

        Returns:
            pd.DataFrame: Tabela ANOVA com os termos até o nível desejado, incluindo coluna "Signif".
        """

        def significance_marker(p):
            if p < 0.001:
                return "***"
            elif p < 0.01:
                return "**"
            elif p < 0.05:
                return "*"
            elif np.isnan(p):
                return ""
            else:
                return "ns"

        terms = []
        for i in range(1, len(self.factors) + 1):
            if max_interaction is not None and i > max_interaction:
                break
            for combo in combinations(self.factors, i):
                terms.append(":".join([f"C({f})" for f in combo]))

        formula = self._get_formula()
        model = smf.ols(formula, data=self.data).fit()
        anova_table = anova_lm(model, typ=2)

        anova_table["Signif"] = anova_table["PR(>F)"].apply(significance_marker)
        return anova_table

    def unfold_interactions(
        self,
        alpha: float = 0.05,
        print_results: bool = True,
        posthoc: str = "tukey",
        max_interaction: int = None,
    ) -> Dict[str, Union[pd.DataFrame, dict]]:
        """
        Desdobra interações até certo nível e aplica testes post hoc.

        Args:
            alpha (float): Nível de significância.
            print_results (bool): Se True, imprime os resultados.
            posthoc (str): Teste post hoc a ser aplicado.
            max_interaction (int): Nível máximo de interação a explorar.

        Returns:
            dict: Resultados da ANOVA e dos testes post hoc.
        """
        anova_table = self.run_anova(max_interaction=max_interaction)
        result = {
            "anova": anova_table,
            "main_effects": {},
            "interactions": {},
        }

        significant_interactions = [
            term
            for term in anova_table.index
            if ":" in term and anova_table.loc[term, "PR(>F)"] <= alpha
        ]

        if not significant_interactions:
            if print_results:
                print(
                    "Sem interações significativas. Aplicando testes post hoc nos efeitos principais."
                )
            for factor in self.factors:
                try:
                    test = PostHocLoader.create(
                        test_name=posthoc,
                        data=self.data,
                        values_column=self.response,
                        trats_column=factor,
                        alpha=alpha,
                    )
                    output = test.run_compact_letters_display()
                    result["main_effects"][factor] = output
                    if print_results:
                        print(f"\nPost hoc ({posthoc}) para {factor}")
                        print(output)
                except Exception as e:
                    if print_results:
                        print(f"Erro ao aplicar post hoc ({posthoc}) em {factor}: {e}")
        else:
            if print_results:
                print(
                    "Interações significativas encontradas. Realizando desdobramentos."
                )
            for term in significant_interactions:
                factors = [f.split("(")[1].strip(")") for f in term.split(":")]
                for f1 in factors:
                    others = [f for f in factors if f != f1]
                    for f2 in others:
                        for level in sorted(self.data[f2].unique()):
                            subset = self.data[self.data[f2] == level]
                            if subset[f1].nunique() <= 1:
                                continue
                            try:
                                model_sub = smf.ols(
                                    f"{self.response} ~ C({f1})", data=subset
                                ).fit()
                                anova_sub = anova_lm(model_sub, typ=2)

                                test_posthoc = PostHocLoader.create(
                                    test_name=posthoc,
                                    data=subset,
                                    values_column=self.response,
                                    trats_column=f1,
                                    alpha=alpha,
                                )
                                posthoc_result = (
                                    test_posthoc.run_compact_letters_display()
                                )

                                key = f"{f1} dentro de {f2}={level}"
                                result["interactions"][key] = {
                                    "anova": anova_sub,
                                    "posthoc": posthoc_result,
                                }

                                if print_results:
                                    print(f"\nDesdobramento: {key}")
                                    print(anova_sub)
                                    print(posthoc_result)
                            except Exception as e:
                                if print_results:
                                    print(
                                        f"Erro ao desdobrar {f1} dentro de {f2}={level}: {e}"
                                    )

        return result

    @staticmethod
    def display_unfolded_interactions(results: dict):
        """
        Exibe de forma organizada os resultados do desdobramento de interações.

        Args:
            results (dict): Saída da função `unfold_interactions`.
        """
        print("\n" + "=" * 50)
        print("📊 ANOVA PRINCIPAL")
        print("=" * 50)
        try:
            print(
                tabulate(results["anova"].round(4), headers="keys", tablefmt="pretty")
            )
        except:
            print(results["anova"])

        if results.get("main_effects"):
            print("\n" + "=" * 50)
            print("🧪 EFEITOS PRINCIPAIS - Post Hoc")
            print("=" * 50)
            for fator, letras in results["main_effects"].items():
                print(f"\n🔹 Fator: {fator}")
                print(letras)

        if results.get("interactions"):
            print("\n" + "=" * 50)
            print("🔬 DESDOBRAMENTOS DE INTERAÇÕES SIGNIFICATIVAS")
            print("=" * 50)
            for label, blocos in results["interactions"].items():
                print(f"\n🧩 {label}")
                print("- ANOVA:")
                try:
                    print(
                        tabulate(
                            blocos["anova"].round(4), headers="keys", tablefmt="github"
                        )
                    )
                except:
                    print(blocos["anova"])
                print("\n- Post hoc:")
                print(blocos["posthoc"])
