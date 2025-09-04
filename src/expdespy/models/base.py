# src/expdespy/models/base.py

from abc import ABC, abstractmethod
from typing import Dict

import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

class ExperimentalDesign(ABC):
    """
    Abstract base class for experimental designs.

    This class provides common methods for statistical analysis,
    such as ANOVA, assumption checking, post hoc testing, and
    visualization of group means.

    Each specific design should inherit from this class and
    implement the abstract method `_get_formula`, which returns
    the statistical formula used for modeling.

    Attributes:
        data (pd.DataFrame): Experimental dataset.
        response (str): Name of the response variable.
        treatment (str): Name of the treatment column.
    """

    def __init__(self, data: pd.DataFrame, response: str, treatment: str):
        self.data = data
        self.response = response
        self.treatment = treatment

    @abstractmethod
    def _get_formula(self) -> str:
        """
        Returns the statistical model formula.

        Must be overridden by each subclass to reflect the
        specific experimental design.

        Returns:
            str: Formula for statistical analysis.
        """
        pass

    def run_anova(self) -> pd.DataFrame:
        """
        Performs Analysis of Variance (ANOVA) using the formula
        defined by the `_get_formula` method.

        Returns:
            pd.DataFrame: ANOVA table of the fitted model (Type II).
        """
        formula = self._get_formula()
        model = smf.ols(formula, data=self.data).fit()

        def significance_marker(p):
            if p < 0.001:
                return "***"
            elif p < 0.01:
                return "**"
            elif p < 0.05:
                return "*"
            elif np.isnan(p):
                return " "
            else:
                return "ns"

        anova_table = anova_lm(model, typ=2)
        # Add significance markers
        anova_table["Signif"] = anova_table["PR(>F)"].apply(significance_marker)

        return anova_table

    def check_assumptions(self, alpha: float = 0.05, print_conclusions: bool = True) -> Dict[str, bool]:
        """
        Checks the assumptions of ANOVA:
        - Normality of residuals (Shapiro-Wilk test)
        - Homoscedasticity (Levene's test)

        Args:
            alpha (float, optional): Significance level. Default is 0.05.
            print_conclusions (bool, optional): If True, prints the test results.

        Returns:
            Dict[str, Dict]: Dictionary containing the results of the tests.
        """
        formula = self._get_formula()
        model = smf.ols(formula, data=self.data).fit()
        residuals = model.resid

        # Normality test
        normality_p = stats.shapiro(residuals).pvalue
        is_normal = normality_p > alpha

        # Homoscedasticity test
        try:
            import re
            factor_names = re.findall(r"C\((\w+)\)", formula)
            if not factor_names:
                factor_names = [self.treatment]
<<<<<<< Updated upstream

<<<<<<< HEAD
=======
            # Agrupar pelos fatores para o teste de Levene
=======
            else:
                factor_names = factor_names[0]
>>>>>>> Stashed changes
>>>>>>> develop
            groups = [
                group[self.response].values
                for _, group in self.data.groupby(factor_names)
            ]
            levene_p = stats.levene(*groups).pvalue
            is_homoscedastic = levene_p > alpha
        except Exception as e:
            levene_p = np.nan
            is_homoscedastic = False
            if print_conclusions:
                print(f"[ERROR while checking homoscedasticity]: {e}")

        if print_conclusions:
            print(f"""
    Normality (Shapiro-Wilk):
        H0: Residuals are normally distributed
        H1: Residuals are not normally distributed
        p-value: {normality_p:.4f}
        Conclusion: H0 {"not rejected" if is_normal else "rejected"}

    Homoscedasticity (Levene):
        H0: Group variances are equal
        H1: Group variances are not equal
        p-value: {levene_p if not np.isnan(levene_p) else 'N/A'}
        Conclusion: H0 {"not rejected" if is_homoscedastic else "rejected"}
    """)

        return {
            "normality (Shapiro-Wilk)": {
                "H0": "Residuals are normally distributed",
                "H1": "Residuals are not normally distributed",
                "p-value": normality_p,
                "Conclusion": "H0 not rejected" if is_normal else "H0 rejected",
            },
            "homoscedasticity (Levene)": {
                "H0": "Group variances are equal",
                "H1": "Group variances are not equal",
                "p-value": levene_p,
                "Conclusion": "H0 not rejected" if is_homoscedastic else "H0 rejected",
            }
        }