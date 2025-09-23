import pandas as pd
import numpy as np
import scipy.stats as stats
from itertools import combinations

from expdespy.posthoc.base import PostHocTest


class LSDTest(PostHocTest):
    """
    Implementation of the Fisher's Least Significant Difference (LSD) test.
    Supports both Student's t-based LSD and Tukey's q-based LSD.
    Requires residual mean square (MSE) and residual degrees of freedom (df_resid).
    """

    def __init__(
        self,
        data: pd.DataFrame,
        values_column: str,
        treatments_column: str,
        anova_table: pd.DataFrame,
        alpha: float = 0.05,
        method: str = "t",  # "t" | "tukey"
    ) -> None:
        super().__init__(data, values_column, treatments_column, alpha)
        self.ssr = anova_table.loc["Residual", "sum_sq"]
        self.df_resid = anova_table.loc["Residual", "df"]
        self.mse = self.ssr / self.df_resid
        self.method = method.lower()

    def run(self) -> pd.DataFrame:
        """
        Run Fisher's LSD test using either Student's t or Tukey's q distribution.

        Returns:
            pd.DataFrame with columns: group1, group2, meandiff, p-value
        """
        results = []
        groups = self.data[self.treatments_column].unique()
        group_means = self.data.groupby(self.treatments_column)[self.values_column].mean()
        group_sizes = self.data[self.treatments_column].value_counts()

        k = len(groups)  # number of groups

        for g1, g2 in combinations(groups, 2):
            mean_diff = group_means[g1] - group_means[g2]
            se = np.sqrt(self.mse * (1 / group_sizes[g1] + 1 / group_sizes[g2]))

            if self.method == "t":
                # Classical LSD using Student's t
                t_stat = mean_diff / se
                pval = 2 * (1 - stats.t.cdf(np.abs(t_stat), df=self.df_resid))
            elif self.method == "tukey":
                # Tukey-adjusted LSD using studentized range q
                q_stat = np.abs(mean_diff) / se * np.sqrt(2)
                # CDF of studentized range distribution
                pval = 1 - stats.studentized_range.cdf(q_stat, k, self.df_resid)
            else:
                raise ValueError("Invalid method. Use 't' or 'tukey'.")

            results.append(
                {
                    "group1": g1,
                    "group2": g2,
                    "meandiff": mean_diff,
                    "p-value": pval,
                }
            )

        return pd.DataFrame(results)

    def _pvalue_column_name(self) -> str:
        return "p-value"