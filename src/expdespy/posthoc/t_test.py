import pandas as pd
import scipy.stats as stats
from itertools import combinations

from expdespy.posthoc.base import PostHocTest


class PairwiseTTest(PostHocTest):
    """
    Implements pairwise independent t-tests between treatments (no correction).
    """

    def __init__(
        self,
        data: pd.DataFrame,
        values_column: str,
        treatments_column: str,
        alpha: float = 0.05,
        # Assume equal variances (default, as in ANOVA)
        equal_var: bool = True
    ) -> None:
        super().__init__(data, values_column, treatments_column, alpha)
        self.equal_var = equal_var

    def run(self) -> pd.DataFrame:
        """
        Runs pairwise independent t-tests for all treatment combinations.

        Returns:
            pd.DataFrame: A DataFrame with the following columns:
                - group1
                - group2
                - meandiff (difference of means)
                - p-value
        """
        results = []
        groups = self.data[self.treatments_column].unique()

        for g1, g2 in combinations(groups, 2):
            vals1 = self.data[self.data[self.treatments_column] == g1][self.values_column]
            vals2 = self.data[self.data[self.treatments_column] == g2][self.values_column]
            stat, pval = stats.ttest_ind(vals1, vals2, equal_var=self.equal_var)

            results.append({
                "group1": g1,
                "group2": g2,
                "meandiff": vals1.mean() - vals2.mean(),
                "p-value": pval
            })

        return pd.DataFrame(results)

    def _pvalue_column_name(self) -> str:
        """
        Returns the column name of the p-value to be used in assign_letters.

        Returns:
            str: "p-value"
        """
        return "p-value"