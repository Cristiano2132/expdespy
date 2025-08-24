import unittest
from expdespy.datasets.dbc_caprinos import load_dbc_caprinos
from expdespy.models import RCBD


class TestDBC(unittest.TestCase):

    def setUp(self):
        # Arrange (setup global)
        self.df, _ = load_dbc_caprinos()
        self.dbc = RCBD(data=self.df, response="ppm_micronutriente",
                    treatment="produto", block="bloco")

    def test_trivial_test(self):
        # Arrange, Act, Assert
        self.assertTrue(True)

    def test_anova_returns_dataframe(self):
        # Arrange
        f_calc_expected = 33.58
        # Act
        result = self.dbc.run_anova()
        f_calc = float(result.loc["C(produto)", "F"])

        # Assert
        self.assertIsInstance(result, type(self.df))
        self.assertIn("F", result.columns)
        self.assertIn("PR(>F)", result.columns)
        self.assertAlmostEqual(f_calc, f_calc_expected, delta=0.1)
