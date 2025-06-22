# src/expdespy/posthoc/base.py

from abc import ABC, abstractmethod
import pandas as pd

class PostHocTest(ABC):
    @abstractmethod
    def compare(self, data: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
        """
        Perform a post-hoc comparison on the given data.

        Parameters:
            data: DataFrame containing the values
            group_col: Column name for group/treatment
            value_col: Column name for response variable

        Returns:
            DataFrame with pairwise comparisons and significance
        """
        pass