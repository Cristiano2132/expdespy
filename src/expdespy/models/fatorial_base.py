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


class FactorialDesign(ExperimentalDesign, ABC):
    """
    Abstract base class for factorial experimental designs.

    This class extends the `ExperimentalDesign` base class to handle
    factorial structures, providing ANOVA, assumption checking,
    interaction unfolding, and post hoc testing.

    Attributes:
        original_factors (List[str]): List of original factor names as provided by the user.
        data (pd.DataFrame): Experimental dataset (a copy of the original).
        factors (List[str]): Sanitized list of factor names used in formulas.
        treatment (str): Statistical treatment formula built from the factors.
        response (str): Name of the response variable.
    """

    def __init__(self, data, response: str, factors: List[str]):
        self.original_factors = factors
        self.data = data.copy()
        self.factors = [self._safe_factor(f) for f in factors]
        treatment_formula = "*".join([f"C({f})" for f in self.factors])
        super().__init__(self.data, response, treatment_formula)

    def _safe_factor(self, factor_name: str) -> str:
        """
        Ensures that factor names do not conflict with Patsy/statsmodels formula syntax.
        For example, renames reserved names like 'C' to 'C_'.

        Args:
            factor_name (str): The factor column name.

        Returns:
            str: A safe factor name for statistical modeling.
        """
        reserved_names = {"C"}  # Add more reserved names here if needed

        if factor_name in reserved_names and factor_name in self.data.columns:
            new_name = factor_name + "_"
            self.data.rename(columns={factor_name: new_name}, inplace=True)
            return new_name

        return factor_name

    @abstractmethod
    def _get_formula(self) -> str:
        """
        Returns the statistical model formula for the factorial design.

        Must be implemented by subclasses.

        Returns:
            str: Formula string for ANOVA.
        """
        pass

    def check_assumptions(
        self, alpha: float = 0.05, print_conclusions: bool = True
    ) -> Dict[str, bool]:
        """
        Checks ANOVA assumptions for factorial designs:
        - Normality of residuals (Shapiro-Wilk test)
        - Homogeneity of variances across factorial combinations (Levene's test)

        Args:
            alpha (float, optional): Significance level. Default is 0.05.
            print_conclusions (bool, optional): If True, prints results.

        Returns:
            Dict[str, bool]: Results of assumption checks.
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
    Assumption checks for factorial design:
    1. Normality of residuals (Shapiro-Wilk)
        - H0: Residuals are normally distributed
        - p-value: {normality_p:.4f}
        - Conclusion: H0 {"not rejected" if is_normal else "rejected"}

    2. Homoscedasticity (Levene)
        - H0: Variances are equal across groups
        - p-value: {levene_p:.4f}
        - Conclusion: H0 {"not rejected" if is_homoscedastic else "rejected"}
            """
            )

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
            },
        }

    def run_anova(self, max_interaction: int = None) -> pd.DataFrame:
        """
        Runs factorial ANOVA, including interactions up to a specified order,
        and adds significance markers (*, **, ***, ns).

        Args:
            max_interaction (int, optional): Maximum interaction order to include
                (1 = main effects, 2 = two-way, ...). If None, all interactions are used.

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
        Unfolds interactions up to a certain order and applies post hoc tests.

        Args:
            alpha (float, optional): Significance level.
            print_results (bool, optional): If True, prints the results.
            posthoc (str, optional): Post hoc test to apply (e.g., "tukey").
            max_interaction (int, optional): Maximum interaction order to explore.

        Returns:
            dict: ANOVA results and post hoc test outputs.
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
                    "No significant interactions. Applying post hoc tests on main effects."
                )
            for factor in self.factors:
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
                        print(f"Error applying post hoc ({posthoc}) to {factor}: {e}")
        else:
            if print_results:
                print("Significant interactions found. Performing unfolding.")
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
                                    treatments_column=f1,
                                    alpha=alpha,
                                )
                                posthoc_result = (
                                    test_posthoc.run_compact_letters_display()
                                )

                                key = f"{f1} within {f2}={level}"
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
                                    print(f"Error unfolding {f1} within {f2}={level}: {e}")

        return result

    @staticmethod
    def display_unfolded_interactions(results: dict):
        """
        Displays unfolded interaction results in an organized format.

        Args:
            results (dict): Output from the `unfold_interactions` method.
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