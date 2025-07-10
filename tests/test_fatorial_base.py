import unittest
import pandas as pd
from expdespy.models.fatorial_base import FatorialDesign

class DummyFatorialDesign(FatorialDesign):
    """Classe auxiliar para testar a FatorialDesign sem dependência de um modelo específico."""
    def _get_formula(self):
        return f"{self.response} ~ " + "*".join(self.factors)

class TestFatorialDesign(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            "f1": ["A", "A", "A", "A", "B", "B", "B", "B"],
            "f2": ["X", "X", "Y", "Y", "X", "X", "Y", "Y"],
            "y": [10, 11, 12, 13, 15, 16, 18, 19]
        })
        self.model = DummyFatorialDesign(
            data=self.data,
            response="y",
            factors=["f1", "f2"]
        )

    def test_formula_generation(self):
        expected_formula = "y ~ f1*f2"
        self.assertEqual(self.model._get_formula(), expected_formula)

    def test_anova_returns_dataframe(self):
        result = self.model.anova()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("PR(>F)", result.columns)

    def test_check_assumptions_returns_dict(self):
        result = self.model.check_assumptions(print_conclusions=False)
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)