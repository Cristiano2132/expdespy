from typing import Optional
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch


def plot_boxplot_with_letters(
    data: pd.DataFrame,
    cld_result: pd.DataFrame,
    values_column: str,
    treatments_column: str,
    hue: Optional[str] = None,
    alpha: float = 0.05,
    figsize: tuple = (12, 6),
    rotation: int = 45,
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """
    Plot a boxplot with treatment means, optional hue,
    and significance letters placed above the boxes.

    Parameters
    ----------
    data : pd.DataFrame
        Original dataset.
    cld_result : pd.DataFrame
        Result from `run_compact_letters_display()`.
        Must include columns [treatments_column, "Letters"].
    values_column : str
        Column containing response variable values.
    treatments_column : str
        Column containing treatment labels.
    hue : str, optional
        Optional column for hue grouping. Default is None.
    alpha : float, optional
        Significance level to display. Default is 0.05.
    figsize : tuple, optional
        Figure size. Default is (12, 6).
    rotation : int, optional
        Rotation angle for x-axis labels. Default is 45.
    ax : matplotlib.axes.Axes, optional
        Axis object to draw the plot on. If None, a new figure is created.

    Returns
    -------
    matplotlib.axes.Axes
        Axis with the boxplot.
    """
    sns.set(style="whitegrid")
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # Order treatments according to CLD result
    order = cld_result[treatments_column].tolist()

    # Draw boxplot
    sns.boxplot(
        data=data,
        x=treatments_column,
        y=values_column,
        hue=hue,
        order=order,
        showfliers=False,
        ax=ax,
    )

    # Compute group statistics
    group_stats = (
        data.groupby(treatments_column)[values_column].agg(["mean", "std"]).reset_index()
    )

    for i, row in cld_result.iterrows():
        group = row[treatments_column]
        letter = row["Letters"]

        mean = group_stats.loc[group_stats[treatments_column] == group, "mean"].values[0]
        std = group_stats.loc[group_stats[treatments_column] == group, "std"].values[0]

        # Add mean marker
        ax.scatter(i, mean, color="black", zorder=10)

        # Position letter slightly above Q3
        q3 = data.loc[data[treatments_column] == group, values_column].quantile(0.75)
        letter_y = q3 + (0.1 * std if not np.isnan(std) else 0.1)

        ax.text(
            i,
            letter_y,
            letter,
            ha="center",
            va="bottom",
            fontsize=12,
            color="black",
        )

    ax.set_xlabel("Treatments")
    ax.set_ylabel(values_column)
    ax.set_title(f"Boxplot with significance letters (α={alpha})")
    plt.setp(ax.get_xticklabels(), rotation=rotation, ha="right")
    return ax

def plot_significance_heatmap(
    df_posthoc: pd.DataFrame,
    treatments: list[str],
    pvalue_col: str = "p-adj",
    alpha_levels: list[float] = [0.01, 0.05, 0.10],
    figsize: tuple = (8, 6),
    ax: Optional[Axes] = None
) -> Axes:
    """
    Plota um heatmap de significância para comparações pareadas entre tratamentos.

    Cada célula indica a significância do p-valor ajustado entre dois tratamentos.
    O heatmap mostra quatro classes:
        - "ns" : não significativo (cinza)
        - "<10%" : p < 0.10 (verde claro)
        - "<5%"  : p < 0.05 (verde médio)
        - "<1%"  : p < 0.01 (verde escuro)

    A diagonal superior é mascarada, e a legenda é posicionada no canto superior
    direito dentro do heatmap, aproveitando o espaço livre.

    Parameters
    ----------
    df_posthoc : pd.DataFrame
        Resultados do teste post-hoc, com colunas ["group1", "group2", pvalue_col].
    treatments : List[str]
        Lista de tratamentos para definir a ordem das linhas e colunas.
    pvalue_col : str, optional
        Nome da coluna contendo os p-valores ajustados. Default é "p-adj".
    alpha_levels : List[float], optional
        Limiares de significância. Default é [0.01, 0.05, 0.10].
    figsize : tuple, optional
        Tamanho da figura (largura, altura). Default é (8, 6).
    ax : Optional[matplotlib.axes.Axes], optional
        Eixo Matplotlib para plotar o heatmap. Se None, cria uma nova figura.

    Returns
    -------
    matplotlib.axes.Axes
        Objeto Axes contendo o heatmap de significância.
    """
    # Cria matriz completa
    mat = pd.DataFrame(np.nan, index=treatments, columns=treatments)
    for _, row in df_posthoc.iterrows():
        g1, g2, pval = row["group1"], row["group2"], row[pvalue_col]
        mat.loc[g1, g2] = pval
        mat.loc[g2, g1] = pval
    np.fill_diagonal(mat.values, 0)  # diagonal opcional: 0 (ns)

    # Mapeia p-values para classes
    def map_class(p: float) -> str:
        if pd.isna(p) or p > alpha_levels[2]:
            return "ns"
        elif p <= alpha_levels[0]:
            return "<1%"
        elif p <= alpha_levels[1]:
            return "<5%"
        elif p <= alpha_levels[2]:
            return "<10%"

    mat_class = mat.applymap(map_class)

    # Define cores
    colors = {
        "ns": "#C5C0C0",    # cinza claro
        "<10%": "#CCF2C4", # verde claro
        "<5%": "#5BB75B",  # verde médio
        "<1%": "#2E7D32",  # verde escuro
    }

    # Converte classes para números
    class_to_num = {"ns":0, "<10%":1, "<5%":2, "<1%":3}
    mat_num = mat_class.replace(class_to_num)

    # Cria colormap e norm
    cmap = mcolors.ListedColormap([colors[k] for k in ["ns","<10%","<5%","<1%"]])
    bounds = [-0.5,0.5,1.5,2.5,3.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # Máscara para a diagonal superior
    mask = np.triu(np.ones_like(mat_num, dtype=bool))

    # Plota heatmap
    sns.heatmap(
        mat_num,
        mask=mask,
        cmap=cmap,
        norm=norm,
        annot=mat_class,
        fmt="",
        square=False,
        linewidths=0.5,
        cbar=False,
        ax=ax,
    )

    # Legenda posicionada dentro do heatmap, no canto superior direito
    legend_elements = [Patch(facecolor=colors[k], edgecolor='k', label=k) for k in ["ns","<10%","<5%","<1%"]]
    ax.legend(
        handles=legend_elements,
        title="Significance",
        title_fontsize=12, 
        loc='upper right',
        bbox_to_anchor=(0.9, 0.9),  # coordenadas relativas ao eixo
        frameon=True,
        borderpad=0.5,
        fontsize=10
    )
    
    # Ajustes estéticos
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.yaxis.grid(True, linestyle="-", linewidth=0.5, alpha=0.3)
    ax.xaxis.grid(True, linestyle="-", linewidth=0.5, alpha=0.3)
    ax.xaxis.tick_bottom()
    ax.xaxis.set_label_position("bottom")
    return ax


if __name__ == "__main__":
    # Example usage
    import pandas as pd
    from expdespy.datasets import load_dic_milho
    from expdespy.posthoc import TukeyHSD

    # Load dataset
    df, _ = load_dic_milho()
    values_column = "produtividade"
    treatments_column = "variedade"

    # Fit Tukey test
    tukey = TukeyHSD(
        df,
        values_column=values_column,
        treatments_column=treatments_column,
    )
    tukey_results = tukey.run()
    tukey_cld = tukey.run_compact_letters_display()
    treatments = df[treatments_column].unique().tolist()

    # Plot boxplot with letters
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    plot_boxplot_with_letters(
        data=df,
        cld_result=tukey_cld,
        values_column=values_column,
        treatments_column=treatments_column,
        ax=ax1,
    )
    plt.show()

    # Plot significance heatmap
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    plot_significance_heatmap(
        df_posthoc=tukey_results,
        treatments=treatments,
        pvalue_col="p-adj",
        ax=ax2,
    )
    plt.show()