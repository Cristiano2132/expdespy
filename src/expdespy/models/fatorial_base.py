# src/expdespy/models/fatorial_base.py

from abc import ABC, abstractmethod
from typing import Dict
from expdespy.models.base import ExperimentalDesign
import scipy.stats as stats
import statsmodels.formula.api as smf


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