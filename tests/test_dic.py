import unittest
from expdespy.datasets.dic_milho import load_dic_milho
from expdespy.models import DIC


class TestDIC(unittest.TestCase):

    def setUp(self):
        # Arrange (global): carregamento dos dados e modelo
        self.df, _ = load_dic_milho()
        self.dic = DIC(data=self.df, response="produtividade",
                    treatment="variedade")

    def test_anova_returns_dataframe(self):
        # Arrange
        f_calc_expected = 7.79

        # Act
        result = self.dic.anova()
        f_calc = float(result.loc["C(variedade)", "F"])

        # Assert
        self.assertIsInstance(result, type(self.df))
        self.assertIn("PR(>F)", result.columns)
        self.assertIn("F", result.columns)
        self.assertIsInstance(f_calc, float)
        self.assertAlmostEqual(f_calc, f_calc_expected, delta=0.01)

    def test_check_assumptions_returns_dict(self):
        # Act
        result = self.dic.check_assumptions()

        # Assert
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)
