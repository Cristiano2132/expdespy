# src/expdespy/utils/diagnostics.py

import numpy as np
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from scipy import stats
from matplotlib import pyplot as plt

def plot_residuals_vs_fitted(model: sm.regression.linear_model.RegressionResultsWrapper, ax: plt.Axes = None) -> plt.Axes:
    """
    Plota Resíduos vs Valores Ajustados para verificar homocedasticidade.
    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Modelo ajustado.
        ax (plt.Axes, optional): Eixos em que plotar. Se None, cria novos eixos.
    Returns:
        plt.Axes: Eixos em que o gráfico foi plotado.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    fitted_vals = model.fittedvalues
    residuals = model.resid

    sns.scatterplot(x=fitted_vals, y=residuals, ax=ax)
    ax.axhline(0, linestyle='--', color='red')
    ax.set_xlabel("Fitted values")
    ax.set_ylabel("Residuals")
    ax.set_title("Residuals vs Fitted")
    return ax


def qq_plot_residuals(model: sm.regression.linear_model.RegressionResultsWrapper, ax: plt.Axes = None) -> plt.Axes:
    """
    Plota o QQ-plot dos resíduos para verificar normalidade.
    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Modelo ajustado.
        ax (plt.Axes, optional): Eixos em que plotar. Se None, cria novos eixos.
    Returns:
        plt.Axes: Eixos em que o gráfico foi plotado.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    sm.qqplot(model.resid, line='s', ax=ax)
    ax.set_title("QQ Plot of Residuals")

    return ax


def plot_residual_hist(model: sm.regression.linear_model.RegressionResultsWrapper, ax: plt.Axes = None) -> plt.Axes:
    """
    Plota histograma e KDE dos resíduos.
    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Modelo ajustado.
        ax (plt.Axes, optional): Eixos em que plotar. Se None, cria novos eixos.

    Returns:
        plt.Axes: Eixos em que o gráfico foi plotado.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    sns.histplot(model.resid, kde=True, ax=ax)
    ax.set_title("Residuals Distribution")
    ax.set_xlabel("Residuals")

    return ax


def cooks_distance_plot(model: sm.regression.linear_model.RegressionResultsWrapper, ax: plt.Axes = None) -> plt.Axes:
    """
    Plota a distância de Cook para identificar pontos influentes.
    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Modelo ajustado.
        ax (plt.Axes, optional): Eixos em que plotar. Se None, cria novos eixos.

    Returns:
        plt.Axes: Eixos em que o gráfico foi plotado.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    influence = model.get_influence()
    cooks_d, _ = influence.cooks_distance

    ax.stem(np.arange(len(cooks_d)), cooks_d, markerfmt=",", basefmt=" ")
    ax.set_xlabel("Observation Index")
    ax.set_ylabel("Cook's Distance")
    ax.set_title("Cook's Distance Plot")

    return ax


def shapiro_test(model: sm.regression.linear_model.RegressionResultsWrapper):
    """
    Executa o teste de Shapiro-Wilk para normalidade dos resíduos.
    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Modelo ajustado.
    Returns:
        dict: Estatística e p-valor do teste de Shapiro-Wilk.
    """
    stat, p_value = stats.shapiro(model.resid)
    return {"statistic": stat, "p_value": p_value}


def breusch_pagan_test(model):
    """
    Executa o teste de Breusch-Pagan para homocedasticidade.
    Retorna estatística LM, p-valor LM, estatística F e p-valor F.
    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Modelo ajustado.
    Returns:
        dict: lm_stat : float
                lagrange multiplier statistic
            - lm_pvalue : float
                p-value of lagrange multiplier test
            - f_stat : float
                f-statistic of the hypothesis that the error variance does not depend on x
            - f_pvalue : float
                p-value for the f-statistic
    """
    lm_stat, lm_pvalue, f_stat, f_pvalue = het_breuschpagan(model.resid, model.model.exog)
    return {
        "lm_stat": lm_stat,
        "lm_pvalue": lm_pvalue,
        "f_stat": f_stat,
        "f_pvalue": f_pvalue
    }


def durbin_watson_test(model: sm.regression.linear_model.RegressionResultsWrapper):
    """
    Executa o teste de Durbin-Watson para autocorrelação dos resíduos.
    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Modelo ajustado.
    Returns:
        float: Valor da estatística do teste de Durbin-Watson.
    """
    return durbin_watson(model.resid)

# if __name__ == "__main__":
#     import matplotlib.pyplot as plt
#     data = sm.datasets.get_rdataset("mtcars").data
#     model = sm.OLS(data["mpg"], sm.add_constant(data[["wt", "hp"]])).fit()

#     fig, axes = plt.subplots(2, 2, figsize=(12, 10))
#     plot_residuals_vs_fitted(model, ax=axes[0, 0])
#     qq_plot_residuals(model, ax=axes[0, 1])
#     plot_residual_hist(model, ax=axes[1, 0])
#     cooks_distance_plot(model, ax=axes[1, 1])
#     plt.tight_layout()
#     plt.show()

#     print("Shapiro-Wilk Test:", shapiro_test(model))
#     print("Breusch-Pagan Test:", breusch_pagan_test(model))
#     print("Durbin-Watson Test:", durbin_watson_test(model))