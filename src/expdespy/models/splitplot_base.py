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
    """
    Abstract base class for Split-Plot experimental designs.

    This class extends the `ExperimentalDesign` base class to handle
    split-plot structures, including assumption checks, ANOVA,
    interaction unfolding, and post hoc testing.

    Attributes:
        data (pd.DataFrame): Experimental dataset (copy of the original).
        main_plot (str): Factor name for the main plot.
        subplot (str): Factor name for the subplot.
        block (str, optional): Factor name for blocks (if provided).
        response (str): Response variable name.
    """

    def __init__(
        self, data, response: str, main_plot: str, subplot: str, block: str = None
    ):
        self.data = data.copy()
        self.main_plot = self._safe_factor(main_plot)
        self.subplot = self._safe_factor(subplot)
        self.block = self._safe_factor(block) if block else None

        treatment_formula = f"C({self.main_plot}) * C({self.subplot})"
        super().__init__(self.data, response, treatment_formula)

    def _safe_factor(self, factor_name: str) -> str:
        """
        Ensures factor names do not conflict with reserved keywords (e.g., "C", "T", "I").

        Args:
            factor_name (str): Original factor name.

        Returns:
            str: Safe factor name (renamed if necessary).
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
        """
        Returns the statistical formula for the split-plot design.

        Must be implemented by subclasses.

        Returns:
            str: Formula string for ANOVA.
        """
        pass

    def check_assumptions(
        self, alpha: float = 0.05, print_conclusions: bool = True
    ) -> Dict[str, bool]:
        """
        Checks ANOVA assumptions for Split-Plot designs:
        - Normality of residuals (Shapiro-Wilk test)
        - Homogeneity of variances across treatment combinations (Levene's test)

        Args:
            alpha (float, optional): Significance level. Default is 0.05.
            print_conclusions (bool, optional): If True, prints conclusions.

        Returns:
            Dict[str, bool]: Results of assumption tests.
        """
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
            print(
                f"""
    ANOVA assumptions (Split-Plot design):
    1. Normality of residuals (Shapiro-Wilk)
        - p-value: {normality_p:.4f}
        - Conclusion: H0 {"not rejected" if is_normal else "rejected"}
    2. Homoscedasticity (Levene)
        - p-value: {levene_p:.4f}
        - Conclusion: H0 {"not rejected" if is_homoscedastic else "rejected"}
            """
            )

        return {
            "normality (Shapiro-Wilk)": {
                "p-value": normality_p,
                "Conclusion": "H0 not rejected" if is_normal else "H0 rejected",
            },
            "homoscedasticity (Levene)": {
                "p-value": levene_p,
                "Conclusion": "H0 not rejected" if is_homoscedastic else "H0 rejected",
            },
        }

    def run_anova(self) -> pd.DataFrame:
        """
        Runs Split-Plot ANOVA and adds significance markers (*, **, ***, ns).

        Returns:
            pd.DataFrame: ANOVA table with significance markers.
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

        formula = self._get_formula()
        model = smf.ols(formula, data=self.data).fit()
        anova_table = anova_lm(model, typ=2)
        anova_table["Signif"] = anova_table["PR(>F)"].apply(significance_marker)
        return anova_table

    def unfold_interactions(
        self, alpha: float = 0.05, print_results: bool = True, posthoc: str = "tukey"
    ) -> Dict[str, Union[pd.DataFrame, dict]]:
        """
        Unfolds significant interactions between main plot and subplot.

        Args:
            alpha (float, optional): Significance level.
            print_results (bool, optional): If True, prints results.
            posthoc (str, optional): Post hoc test to apply. Default is "tukey".

        Returns:
            dict: Results including ANOVA, main effects, and interactions.
        """
        anova_table = self.run_anova()
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
                    "No significant interactions. Applying post hoc tests to main effects."
                )
            for factor in [self.main_plot, self.subplot]:
                try:
                    test = PostHocLoader.create(
                        test_name=posthoc,
                        data=self.data,
                        values_column=self.response,
                        treatments_column=factor,
                        alpha=alpha,
                    )
                    output = test.run_compact_letters_display()
                    result["main_effects"][factor] = output
                    if print_results:
                        print(f"\nPost hoc ({posthoc}) for {factor}")
                        print(output)
                except Exception as e:
                    if print_results:
                        print(f"Error applying post hoc for {factor}: {e}")
        else:
            if print_results:
                print("Significant interactions found. Performing unfolding.")
            # Example: unfold subplot within each level of the main plot
            for level in sorted(self.data[self.main_plot].unique()):
                subset = self.data[self.data[self.main_plot] == level]
                try:
                    model_sub = smf.ols(
                        f"{self.response} ~ C({self.subplot})", data=subset
                    ).fit()
                    anova_sub = anova_lm(model_sub, typ=2)

                    test_posthoc = PostHocLoader.create(
                        test_name=posthoc,
                        data=subset,
                        values_column=self.response,
                        treatments_column=self.subplot,
                        alpha=alpha,
                    )
                    posthoc_result = test_posthoc.run_compact_letters_display()

                    key = f"{self.subplot} within {self.main_plot}={level}"
                    result["interactions"][key] = {
                        "anova": anova_sub,
                        "posthoc": posthoc_result,
                    }

                    if print_results:
                        print(f"\nUnfolding: {key}")
                        print(anova_sub)
                        print(posthoc_result)
                except Exception as e:
                    if print_results:
                        print(f"Error unfolding {key}: {e}")

        return result

    @staticmethod
    def display_unfolded_interactions(results: dict):
        """
        Displays unfolded interaction results in an organized format.

        Args:
            results (dict): Output of the `unfold_interactions` method.
        """
        print("\n" + "=" * 50)
        print("📊 MAIN ANOVA")
        print("=" * 50)
        try:
            print(
                tabulate(results["anova"].round(4), headers="keys", tablefmt="pretty")
            )
        except:
            print(results["anova"])

        if results.get("main_effects"):
            print("\n" + "=" * 50)
            print("🧪 MAIN EFFECTS - Post Hoc")
            print("=" * 50)
            for factor, letters in results["main_effects"].items():
                print(f"\n🔹 Factor: {factor}")
                print(letters)

        if results.get("interactions"):
            print("\n" + "=" * 50)
            print("🔬 SIGNIFICANT INTERACTIONS - Unfolding")
            print("=" * 50)
            for label, blocks in results["interactions"].items():
                print(f"\n🧩 {label}")
                print("- ANOVA:")
                try:
                    print(
                        tabulate(
                            blocks["anova"].round(4), headers="keys", tablefmt="github"
                        )
                    )
                except:
                    print(blocks["anova"])
                print("\n- Post hoc:")
                print(blocks["posthoc"])
