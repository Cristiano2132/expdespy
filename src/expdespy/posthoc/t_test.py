import pandas as pd
import scipy.stats as stats
from itertools import combinations

from expdespy.posthoc.base import PostHocTest


class PairwiseTTest(PostHocTest):
    """
    Implementation of uncorrected pairwise t-tests between treatments.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        values_column: str,
        treatments_column: str,
        alpha: float = 0.05,
        equal_var: bool = True,
    ) -> None:
        super().__init__(data, values_column, treatments_column, alpha)
        self.equal_var = equal_var

    def run(self) -> pd.DataFrame:
        """
        Run t-tests for all treatment pairs.

        Returns:
            pd.DataFrame with columns: group1, group2, meandiff, p-value
        """
        results = []
        groups = self.data[self.treatments_column].unique()

        for g1, g2 in combinations(groups, 2):
            vals1 = self.data[self.data[self.treatments_column] == g1][
                self.values_column
            ]
            vals2 = self.data[self.data[self.treatments_column] == g2][
                self.values_column
            ]
            _, pval = stats.ttest_ind(vals1, vals2, equal_var=self.equal_var)

            results.append(
                {
                    "group1": g1,
                    "group2": g2,
                    "meandiff": vals1.mean() - vals2.mean(),
                    "p-value": pval,
                }
            )

        return pd.DataFrame(results)

    def _pvalue_column_name(self) -> str:
        return "p-value"