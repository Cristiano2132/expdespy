import unittest
import pandas as pd
import statsmodels.formula.api as smf
from expdespy.regressao import diagnostics as diag
from matplotlib import pyplot as plt

class TestDiagnostics(unittest.TestCase):

    def setUp(self):
        # Arrange: cria dados artificiais para regressão simples
        self.df = pd.DataFrame({
            "y": [4, 6, 7, 9, 10, 13, 15, 16, 18, 20],
            "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        })
        self.model = smf.ols("y ~ x", data=self.df).fit()

    def test_plot_residuals_vs_fitted(self):
        # Act + Assert: apenas verifica se roda sem erro
        ax = diag.plot_residuals_vs_fitted(self.model)
        self.assertIsInstance(ax, plt.Axes)

    def test_qq_plot_residuals(self):
        ax = diag.qq_plot_residuals(self.model)
        self.assertIsInstance(ax, plt.Axes)

    def test_plot_residual_hist(self):
        ax = diag.plot_residual_hist(self.model)
        self.assertIsInstance(ax, plt.Axes)

    def test_cooks_distance_plot(self):
        ax = diag.cooks_distance_plot(self.model)
        self.assertIsInstance(ax, plt.Axes)

    def test_shapiro_test_returns_dict(self):
        result = diag.shapiro_test(self.model)
        self.assertIsInstance(result, dict)
        self.assertIn("statistic", result)
        self.assertIn("p_value", result)

    def test_breusch_pagan_test_returns_dict(self):
        result = diag.breusch_pagan_test(self.model)
        self.assertIsInstance(result, dict)
        self.assertIn("lm_stat", result)
        self.assertIn("lm_pvalue", result)
        self.assertIn("f_stat", result)
        self.assertIn("f_pvalue", result)

    def test_durbin_watson_test_returns_float(self):
        result = diag.durbin_watson_test(self.model)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 4)
