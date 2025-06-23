# src/expdespy/posthoc/ttest.py

import pandas as pd
import scipy.stats as stats
from itertools import combinations

from expdespy.posthoc.base import PostHocTest


class PairwiseTTest(PostHocTest):
    """
    Implementa o teste t pareado entre pares de tratamentos (sem correção).
    """

    def __init__(
        self,
        data: pd.DataFrame,
        values_column: str,
        trats_column: str,
        alpha: float = 0.05,
        # Assume variâncias iguais (padrão como no ANOVA)
        equal_var: bool = True
    ) -> None:
        super().__init__(data, values_column, trats_column, alpha)
        self.equal_var = equal_var

    def run(self) -> pd.DataFrame:
        """
        Executa o teste t para todas as comparações entre pares de tratamentos.

        Returns:
            pd.DataFrame com as colunas: group1, group2, meandiff, p-value
        """
        results = []
        groups = self.data[self.trats_column].unique()

        for g1, g2 in combinations(groups, 2):
            vals1 = self.data[self.data[self.trats_column]
                              == g1][self.values_column]
            vals2 = self.data[self.data[self.trats_column]
                              == g2][self.values_column]
            stat, pval = stats.ttest_ind(
                vals1, vals2, equal_var=self.equal_var)

            results.append({
                "group1": g1,
                "group2": g2,
                "meandiff": vals1.mean() - vals2.mean(),
                "p-value": pval
            })

        return pd.DataFrame(results)

    def _pvalue_column_name(self) -> str:
        """
        Informa o nome da coluna de p-valor a ser usada no assign_letters.

        Returns:
            str: "p-value"
        """
        return "p-value"
