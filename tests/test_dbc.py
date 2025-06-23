# import unittest
import unittest
from matplotlib import pyplot as plt
from expdespy.datasets.dbc_caprinos import load_dbc_caprinos
from expdespy.models import DBC



class TestDBC(unittest.TestCase):

    def setUp(self):
        # Arrange (setup global)
        self.df, _ = load_dbc_caprinos()
        self.dbc = DBC(data=self.df, response="ppm_micronutriente", treatment="produto", block="bloco")

    def test_trivial_test(self):
        # Arrange, Act, Assert
        self.assertTrue(True)

    def test_anova_returns_dataframe(self):
        # Arrange
        f_calc_expected = 33.58
        # Act
        result = self.dbc.anova()
        f_calc = float(result.loc["C(produto)", "F"])

        # Assert
        self.assertIsInstance(result, type(self.df))
        self.assertIn("F", result.columns)
        self.assertIn("PR(>F)", result.columns)
        self.assertAlmostEqual(f_calc, f_calc_expected, delta=0.1)

    # def test_posthoc_returns_dataframe(self):
    #     # Act
    #     result = self.dbc.posthoc(method="tukey")

    #     # Assert
    #     self.assertIsInstance(result, type(self.df))
    #     self.assertIn("group1", result.columns)
    #     self.assertIn("group2", result.columns)
    #     self.assertIn("reject", result.columns)

    # def test_plot_means_runs(self):
    #     # Arrange
    #     fig, ax = plt.subplots()

    #     # Act & Assert
    #     try:
    #         self.dbc.plot_means(ax=ax)
    #     except Exception as e:
    #         self.fail(f"plot_means() raised an exception: {e}")

    def test_check_assumptions_returns_dict(self):
        # Act
        result = self.dbc.check_assumptions()

        # Assert
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)