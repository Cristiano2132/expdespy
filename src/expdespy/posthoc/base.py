# src/expdespy/posthoc/base.py

from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from expdespy.utils.utils import assign_letters


class PostHocTest(ABC):
    """
    Abstract base class for post hoc tests.

    This class defines the general structure for running post hoc tests
    and displaying results with compact letter displays (CLD).
    """

    def __init__(
        self,
        data: pd.DataFrame,
        values_column: str,
        treatments_column: str,
        alpha: float = 0.05,
    ) -> None:
        """
        Initialize a PostHocTest instance.

        Args:
            data (pd.DataFrame): Experimental dataset.
            values_column (str): Column containing response variable values.
            treatments_column (str): Column containing treatment labels.
            alpha (float, optional): Significance level for tests. Default is 0.05.
        """
        self.data = data
        self.values_column = values_column
        self.treatments_column = treatments_column
        self.alpha = alpha

    @abstractmethod
    def run(self) -> pd.DataFrame:
        """
        Run the post hoc test.

        Returns:
            pd.DataFrame: A DataFrame containing test results
                        (group comparisons and p-values).
        """
        pass

    @abstractmethod
    def _pvalue_column_name(self) -> str:
        """
        Return the column name used for p-values in the DataFrame
        returned by `run()`.

        Returns:
            str: Name of the p-value column.
        """
        pass

    def run_compact_letters_display(self) -> pd.DataFrame:
        """
        Run the post hoc test and return a compact letter display (CLD).

        The method calculates treatment means and assigns significance
        letters based on pairwise comparisons.

        Returns:
            pd.DataFrame: A DataFrame with treatment means and assigned letters.
        """
        df_posthoc = self.run()

        cld_result = assign_letters(
            df_post_hoc=df_posthoc,
            G1="group1",
            G2="group2",
            P=self._pvalue_column_name(),
            alpha=self.alpha,
            order="descending",
            data=self.data,
            vals=self.values_column,
            group=self.treatments_column,
        )

        means = (
            self.data.groupby(self.treatments_column)[self.values_column]
            .mean()
            .rename("Mean")
        )

        final_result = pd.concat([means, cld_result], axis=1).reset_index()
        final_result.rename(columns={"index": self.treatments_column}, inplace=True)
        final_result.sort_values(by="Mean", ascending=False, inplace=True)
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
            self.data.groupby(self.treatments_column)[self.values_column]
            .agg(["mean", "max"])
            .rename(columns={"mean": "Mean", "max": "Max"})
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
                color="black",
            )

        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.yaxis.grid(True, linestyle="-", linewidth=0.5)
        ax.set_title("Treatment means with significance letters")
