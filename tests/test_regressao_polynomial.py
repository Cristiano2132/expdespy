import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from expdespy.regressao import PolynomialRegression


class TestPolynomialRegression(unittest.TestCase):

    def setUp(self):
        # Dados artificiais para um padrão quadrático
        np.random.seed(42)
        self.df = pd.DataFrame({
            "dose": np.linspace(0, 5, 6),
            "yield": [5, 7, 9, 15, 18, 20]
        })
        self.poly = PolynomialRegression(
            data=self.df,
            response="yield",
            factor="dose"
        )

    def test_fit_degree_2_returns_results(self):
        # Act
        results = self.poly.fit(degree=2)

        # Assert
        self.assertIsInstance(
            results, sm.regression.linear_model.RegressionResultsWrapper
        )
        self.assertEqual(len(results.params), 3)  # β0, β1, β2
        self.assertIn("dose^2", self.poly.data.columns)

    def test_anova_returns_dataframe(self):
        # Arrange
        self.poly.fit(degree=2)

        # Act
        anova_df = self.poly.anova()

        # Assert
        self.assertIsInstance(anova_df, pd.DataFrame)
        self.assertIn("sum_sq", anova_df.columns)

    def test_anova_raises_if_not_fitted(self):
        with self.assertRaises(ValueError):
            self.poly.anova()

    def test_plot_returns_axes(self):
        # Arrange
        self.poly.fit(degree=2)
        fig, ax = plt.subplots()

        # Act
        returned_ax = self.poly.plot(ax=ax)

        # Assert
        self.assertIs(returned_ax, ax)
        self.assertEqual(len(ax.lines), 1)   # Linha do ajuste
        self.assertEqual(len(ax.collections), 1)  # Pontos scatter

    def test_fit_degree_1_no_extra_columns(self):
        # Act
        self.poly.fit(degree=1)

        # Assert
        extra_cols = [c for c in self.poly.data.columns if "^" in c]
        self.assertEqual(len(extra_cols), 0)

    def test_fit_with_invalid_degree(self):
        with self.assertRaises(ValueError):
            self.poly.fit(degree=0)  # não permitido, ajuste seu método se quiser suportar
