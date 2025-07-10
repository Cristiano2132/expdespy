import unittest
from expdespy.datasets import load_fatorial_dic_nitrogenio_fosforo
from expdespy.models import FatorialDIC  # Ou FatorialDesignDIC, dependendo do seu nome
import pandas as pd


class TestFatorialDIC(unittest.TestCase):

    def setUp(self):
        # Arrange
        self.df, description = load_fatorial_dic_nitrogenio_fosforo()
        factors = description.get("factors")
        response = description.get("response")
        self.model = FatorialDIC(data=self.df, response=response, factors=factors)

    def test_anova_returns_dataframe(self):
        # Act
        result = self.model.anova()
        f_calc_axb = float(result.loc["C(f1):C(f2)", "F"])
        f_calc_axb_esperado = 4.95
        # Assert
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("PR(>F)", result.columns)
        self.assertIn("F", result.columns)
        self.assertAlmostEqual(f_calc_axb, f_calc_axb_esperado, delta=0.1)

    def test_check_assumptions_returns_dict(self):
        # Act
        result = self.model.check_assumptions(print_conclusions=False)

        # Assert
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)

