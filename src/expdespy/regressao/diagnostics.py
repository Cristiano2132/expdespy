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
    Plot Residuals vs Fitted values to check for homoscedasticity.

    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Fitted model.
        ax (plt.Axes, optional): Axes object to plot on. If None, creates a new one.

    Returns:
        plt.Axes: The axes with the plotted graph.
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
    Plot the QQ-plot of residuals to check normality.

    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Fitted model.
        ax (plt.Axes, optional): Axes object to plot on. If None, creates a new one.

    Returns:
        plt.Axes: The axes with the plotted graph.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    sm.qqplot(model.resid, line='s', ax=ax)
    ax.set_title("QQ Plot of Residuals")

    return ax


def plot_residual_hist(model: sm.regression.linear_model.RegressionResultsWrapper, ax: plt.Axes = None) -> plt.Axes:
    """
    Plot histogram and KDE of residuals.

    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Fitted model.
        ax (plt.Axes, optional): Axes object to plot on. If None, creates a new one.

    Returns:
        plt.Axes: The axes with the plotted graph.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    sns.histplot(model.resid, kde=True, ax=ax)
    ax.set_title("Residuals Distribution")
    ax.set_xlabel("Residuals")

    return ax


def cooks_distance_plot(model: sm.regression.linear_model.RegressionResultsWrapper, ax: plt.Axes = None) -> plt.Axes:
    """
    Plot Cook's Distance to identify influential observations.

    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Fitted model.
        ax (plt.Axes, optional): Axes object to plot on. If None, creates a new one.

    Returns:
        plt.Axes: The axes with the plotted graph.
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
    Perform the Shapiro-Wilk test for normality of residuals.

    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Fitted model.

    Returns:
        dict: Dictionary containing test statistic and p-value.
    """
    stat, p_value = stats.shapiro(model.resid)
    return {"statistic": stat, "p_value": p_value}


def breusch_pagan_test(model: sm.regression.linear_model.RegressionResultsWrapper):
    """
    Perform the Breusch-Pagan test for homoscedasticity.

    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Fitted model.

    Returns:
        dict: Contains:
            - lm_stat (float): Lagrange multiplier statistic.
            - lm_pvalue (float): p-value of the Lagrange multiplier test.
            - f_stat (float): F-statistic for the null hypothesis that error variance does not depend on x.
            - f_pvalue (float): p-value of the F-statistic.
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
    Perform the Durbin-Watson test for autocorrelation of residuals.

    Args:
        model (sm.regression.linear_model.RegressionResultsWrapper): Fitted model.

    Returns:
        float: Durbin-Watson test statistic.
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