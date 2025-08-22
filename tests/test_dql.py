import unittest
from expdespy.datasets import load_dql_cana
from expdespy.models import LSD


class TestDQL(unittest.TestCase):

    def setUp(self):
        # Arrange (setup global)
        self.df, _ = load_dql_cana()
        self.dql = LSD(data=self.df, response="resposta", treatment="tratamento", block_row="linha", block_col="coluna")

    def test_trivial_test(self):
        # Arrange, Act, Assert
        self.assertTrue(True)

    def test_anova_returns_dataframe(self):
        # Arrange
        f_calc_expected = 12.09 
        # Act
        result = self.dql.anova()
        f_calc = float(result.loc["C(tratamento)", "F"])

        # Assert
        self.assertIsInstance(result, type(self.df))
        self.assertIn("F", result.columns)
        self.assertIn("PR(>F)", result.columns)
        self.assertAlmostEqual(f_calc, f_calc_expected, delta=0.1)
