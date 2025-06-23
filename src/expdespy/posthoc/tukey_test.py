# src/expdespy/posthoc/tukey.py

import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from expdespy.posthoc.base import PostHocTest


class TukeyHSD(PostHocTest):
    """
    Implementação do teste post hoc de Tukey HSD.
    Herda comportamento padrão de exibição compacta e plotagem da superclasse.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        values_column: str,
        trats_column: str,
        alpha: float = 0.05
    ) -> None:
        super().__init__(data, values_column, trats_column, alpha)

    def run(self) -> pd.DataFrame:
        """
        Executa o teste de Tukey HSD e retorna os resultados como um DataFrame.

        Returns:
            pd.DataFrame: Resultados do teste de comparações múltiplas de Tukey.
        """
        tukey_result = pairwise_tukeyhsd(
            endog=self.data[self.values_column],
            groups=self.data[self.trats_column].astype(str),
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
        Informa o nome da coluna de p-valor usada para a verificação de significância.

        Returns:
            str: Nome da coluna de p-valor ('p-adj').
        """
        return "p-adj"
