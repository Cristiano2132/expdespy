# src/expdespy/posthoc/base.py

from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from expdespy.utils.utils import assign_letters


class PostHocTest(ABC):
    def __init__(self,
                data: pd.DataFrame,
                values_column: str,
                trats_column: str,
                alpha: float = 0.05) -> None:
        self.data = data
        self.values_column = values_column
        self.trats_column = trats_column
        self.alpha = alpha

    @abstractmethod
    def run(self) -> pd.DataFrame:
        """
        Executa o teste post hoc e retorna um DataFrame com os resultados.
        """
        pass

    @abstractmethod
    def _pvalue_column_name(self) -> str:
        """
        Retorna o nome da coluna de p-valor no DataFrame retornado por `run()`.
        """
        pass

    def run_compact_letters_display(self) -> pd.DataFrame:
        """
        Executa o teste post hoc e retorna um DataFrame com as médias ordenadas
        e as letras para a apresentação compacta.
        """
        df_posthoc = self.run()

        cld_result = assign_letters(
            df_post_hoc=df_posthoc,
            G1='group1',
            G2='group2',
            P=self._pvalue_column_name(),
            alpha=self.alpha,
            order='descending',
            data=self.data,
            vals=self.values_column,
            group=self.trats_column
        )

        means = self.data.groupby(self.trats_column)[
            self.values_column].mean().rename('Mean')
        final_result = pd.concat([means, cld_result], axis=1).reset_index()
        final_result.rename(columns={'index': self.trats_column}, inplace=True)
        final_result.sort_values(by='Mean', ascending=False, inplace=True)
        return final_result

    def plot_compact_letters_display(
        self, ax: Optional[plt.Axes] = None, points_color: str = None, hue: str = None, palette: str = "Blues", order_by: str = None
    ) -> None:
        """
        Plot a boxplot with compact letter display (CLD).

        Args:
            ax (matplotlib.axes.Axes, optional): Axis object to draw the plot on.
                                                If None, a new figure is created.
            points_color (str, optional): Color for individual data points. Default is None. If None, will not plot points.
            hue (str, optional): Column name for hue grouping in the boxplot. Default is None.
            palette (str, optional): Color palette for the boxplot. Default is "Blues".
            order_by (str, optional): Column name to order treatments by. Default is None. If None, treatments are ordered by mean values.
        """
        cld_result = self.run_compact_letters_display()
        sns.set_style("whitegrid")
        group_stats = (
            self.data.groupby(self.trats_column)[self.values_column]
            .agg(['mean', 'max'])
            .rename(columns={'mean': 'Mean', 'max': 'Max'})
            .reset_index()
        )
        cld_plot_df = cld_result.merge(group_stats, on=self.treatments_column)
        if order_by is not None and order_by in cld_plot_df.columns:
            ordered_groups = cld_plot_df.sort_values(by=order_by, ascending=True)[self.treatments_column].tolist()
        else:
            ordered_groups = cld_plot_df.sort_values(by="Mean", ascending=True)[self.treatments_column].tolist()

        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))

        if hue is not None and hue in self.data.columns:
            sns.boxplot(
                data=self.data,
                x=self.treatments_column,
                y=self.values_column,
                hue=hue,
                order=ordered_groups,
                palette=palette,
                ax=ax,
                legend=False,
            )
        else:
            sns.boxplot(
                data=self.data,
                x=self.treatments_column,
                y=self.values_column,
                order=ordered_groups,
                palette=palette,
                ax=ax,
                hue=self.treatments_column,
                legend=False,
            )
        if points_color is not None:
            sns.stripplot(
                data=self.data,
                x=self.treatments_column,
                y=self.values_column,
                order=ordered_groups,
                dodge=True,
                color=points_color,
                size=5,
                ax=ax,
            )

        for i, row in cld_plot_df.iterrows():
            ax.text(
                x=i,
                y=row["Max"] + 0.1,
                s=row["Letters"],
                ha="center",
                va="bottom",
                fontsize=12,
                color="black"
            )

        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.yaxis.grid(True, linestyle='-', linewidth=0.5)
        ax.set_title("Médias por tratamento com letras de significância")
