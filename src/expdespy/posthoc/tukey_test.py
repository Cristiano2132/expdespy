import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from expdespy.posthoc.base import PostHocTest


class TukeyHSD(PostHocTest):
    """
    Implementation of the Tukey HSD post hoc test.
    """

    def run(self) -> pd.DataFrame:
        """
        Run Tukey's HSD and return results.

        Returns:
            pd.DataFrame with columns: group1, group2, meandiff, p-adj, lower, upper, reject
        """
        tukey_result = pairwise_tukeyhsd(
            endog=self.data[self.values_column],
            groups=self.data[self.treatments_column].astype(str),
            alpha=self.alpha,
        )
        df = pd.DataFrame(
            tukey_result._results_table.data[1:],  # skip header row
            columns=tukey_result._results_table.data[0],
        )
        df.columns = [
            "group1",
            "group2",
            "meandiff",
            "p-adj",
            "lower",
            "upper",
            "reject",
        ]
        return df

    def _pvalue_column_name(self) -> str:
        return "p-adj"