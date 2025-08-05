# src/expdespy/models/splitplot_base.py

from abc import ABC, abstractmethod
from typing import Dict, Union
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from tabulate import tabulate
from expdespy.models.base import ExperimentalDesign
from expdespy.posthoc import PostHocLoader

class SplitPlotDesign(ExperimentalDesign, ABC):
    def __init__(self, data, response: str, main_plot: str, subplot: str, block: str = None):
        self.data = data.copy()
        self.main_plot = self._safe_factor(main_plot)
        self.subplot = self._safe_factor(subplot)
        self.block = self._safe_factor(block) if block else None

        treatment_formula = f"C({self.main_plot}) * C({self.subplot})"
        super().__init__(self.data, response, treatment_formula)

    def _safe_factor(self, factor_name: str) -> str:
        """
        Renomeia o fator no DataFrame caso tenha um nome reservado (ex: "C").

        Args:
            factor_name (str): Nome do fator original.

        Returns:
            str: Nome seguro do fator (talvez renomeado).
        """
        reserved = {"C": "C_", "T": "T_", "I": "I_"}
        if not factor_name:
            return factor_name

        if factor_name in reserved:
            safe_name = reserved[factor_name]
            if factor_name in self.data.columns:
                self.data.rename(columns={factor_name: safe_name}, inplace=True)
            return safe_name
        return factor_name
    
    @abstractmethod
    def _get_formula(self) -> str:
        pass

    def check_assumptions(self, alpha: float = 0.05, print_conclusions: bool = True) -> Dict[str, bool]:
        formula = self._get_formula()
        model = smf.ols(formula, data=self.data).fit()
        residuals = model.resid

        normality_p = stats.shapiro(residuals).pvalue
        is_normal = normality_p > alpha

        groups = [
            group[self.response].values
            for _, group in self.data.groupby([self.main_plot, self.subplot])
        ]
        levene_p = stats.levene(*groups).pvalue
        is_homoscedastic = levene_p > alpha

        if print_conclusions:
            print(f"""
    Pressupostos ANOVA (Parcela Subdividida):
    1. Normalidade dos resíduos (Shapiro-Wilk)
        - p-valor: {normality_p:.4f}
        - Conclusão: H0 {'não rejeitada' if is_normal else 'rejeitada'}
    2. Homocedasticidade (Levene)
        - p-valor: {levene_p:.4f}
        - Conclusão: H0 {'não rejeitada' if is_homoscedastic else 'rejeitada'}
            """)

        return {
            "normality (Shapiro-Wilk)": {
                "p-value": normality_p,
                "Conclusion": "H0 não rejeitada" if is_normal else "H0 rejeitada",
            },
            "homoscedasticity (Levene)": {
                "p-value": levene_p,
                "Conclusion": "H0 não rejeitada" if is_homoscedastic else "H0 rejeitada",
            }
        }

    def run_anova(self) -> pd.DataFrame:
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

        formula = self._get_formula()
        model = smf.ols(formula, data=self.data).fit()
        anova_table = anova_lm(model, typ=2)
        anova_table["Signif"] = anova_table["PR(>F)"].apply(significance_marker)
        return anova_table

    def unfold_interactions(
        self,
        alpha: float = 0.05,
        print_results: bool = True,
        posthoc: str = "tukey"
    ) -> Dict[str, Union[pd.DataFrame, dict]]:
        """
        Desdobra interações significativas entre parcela e subparcela.
        """
        anova_table = self.run_anova()
        result = {
            "anova": anova_table,
            "main_effects": {},
            "interactions": {},
        }

        significant_interactions = [
            term for term in anova_table.index
            if ":" in term and anova_table.loc[term, "PR(>F)"] <= alpha
        ]

        if not significant_interactions:
            if print_results:
                print("Sem interações significativas. Aplicando testes post hoc nos efeitos principais.")
            for factor in [self.main_plot, self.subplot]:
                try:
                    test = PostHocLoader.create(
                        test_name=posthoc,
                        data=self.data,
                        values_column=self.response,
                        trats_column=factor,
                        alpha=alpha
                    )
                    output = test.run_compact_letters_display()
                    result["main_effects"][factor] = output
                    if print_results:
                        print(f"\nPost hoc ({posthoc}) para {factor}")
                        print(output)
                except Exception as e:
                    if print_results:
                        print(f"Erro ao aplicar post hoc para {factor}: {e}")
        else:
            if print_results:
                print("Interações significativas encontradas. Realizando desdobramentos.")
            # Exemplo: desdobrar subplot dentro de cada nível da main_plot
            for level in sorted(self.data[self.main_plot].unique()):
                subset = self.data[self.data[self.main_plot] == level]
                try:
                    model_sub = smf.ols(f"{self.response} ~ C({self.subplot})", data=subset).fit()
                    anova_sub = anova_lm(model_sub, typ=2)

                    test_posthoc = PostHocLoader.create(
                        test_name=posthoc,
                        data=subset,
                        values_column=self.response,
                        trats_column=self.subplot,
                        alpha=alpha
                    )
                    posthoc_result = test_posthoc.run_compact_letters_display()

                    key = f"{self.subplot} dentro de {self.main_plot}={level}"
                    result["interactions"][key] = {
                        "anova": anova_sub,
                        "posthoc": posthoc_result
                    }

                    if print_results:
                        print(f"\nDesdobramento: {key}")
                        print(anova_sub)
                        print(posthoc_result)
                except Exception as e:
                    if print_results:
                        print(f"Erro ao desdobrar {key}: {e}")

        return result

    @staticmethod
    def display_unfolded_interactions(results: dict):
        """
        Exibe de forma organizada os resultados do desdobramento de interações.

        Args:
            results (dict): Saída da função `unfold_interactions`.
        """
        print("\n" + "="*50)
        print("📊 ANOVA PRINCIPAL")
        print("="*50)
        try:
            print(tabulate(results["anova"].round(4), headers="keys", tablefmt="pretty"))
        except:
            print(results["anova"])

        if results.get("main_effects"):
            print("\n" + "="*50)
            print("🧪 EFEITOS PRINCIPAIS - Post Hoc")
            print("="*50)
            for fator, letras in results["main_effects"].items():
                print(f"\n🔹 Fator: {fator}")
                print(letras)

        if results.get("interactions"):
            print("\n" + "="*50)
            print("🔬 DESDOBRAMENTOS DE INTERAÇÕES SIGNIFICATIVAS")
            print("="*50)
            for label, blocos in results["interactions"].items():
                print(f"\n🧩 {label}")
                print("- ANOVA:")
                try:
                    print(tabulate(blocos["anova"].round(4), headers="keys", tablefmt="github"))
                except:
                    print(blocos["anova"])
                print("\n- Post hoc:")
                print(blocos["posthoc"])