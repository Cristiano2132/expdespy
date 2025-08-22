import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from expdespy.posthoc.base import PostHocTest


class TukeyHSD(PostHocTest):
    """
    Implementation of the Tukey HSD post hoc test.
    Inherits compact letter display and plotting behavior from the superclass.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        values_column: str,
        treatments_column: str,
        alpha: float = 0.05
    ) -> None:
        super().__init__(data, values_column, treatments_column, alpha)

    def run(self) -> pd.DataFrame:
        """
        Runs the Tukey HSD test and returns the results as a DataFrame.

        Returns:
            pd.DataFrame: Results of Tukey's multiple comparison test with columns:
                - group1
                - group2
                - meandiff
                - p-adj
                - lower
                - upper
                - reject
        """
        tukey_result = pairwise_tukeyhsd(
            endog=self.data[self.values_column],
            groups=self.data[self.treatments_column].astype(str),
            alpha=self.alpha
        )
        df = pd.DataFrame(
            tukey_result._results_table.data[1:],
            columns=tukey_result._results_table.data[0]
        )
        df.columns = ['group1', 'group2', 'meandiff',
                    'p-adj', 'lower', 'upper', 'reject']
        return df

    def _pvalue_column_name(self) -> str:
        """
        Returns the name of the p-value column used for significance testing.

        Returns:
            str: "p-adj"
        """
        return "p-adj"