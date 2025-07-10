# tests/test_base_model.py

import unittest
import pandas as pd
from expdespy.models.base import ExperimentalDesign

class DummyDesign(ExperimentalDesign):
    def _get_formula(self) -> str:
        return f"{self.response} ~ C({self.treatment})"

class TestExperimentalDesign(unittest.TestCase):

    def setUp(self):
        # Criando dados simples para teste
        self.df = pd.DataFrame({
            "tratamento": ["A", "A", "B", "B", "C", "C"],
            "resposta": [10, 12, 14, 13, 11, 10]
        })
        self.model = DummyDesign(data=self.df, response="resposta", treatment="tratamento")

    def test_anova_runs(self):
        anova_table = self.model.anova()
        self.assertIn("PR(>F)", anova_table.columns)
        self.assertIn("Signif", anova_table.columns)
        self.assertTrue(len(anova_table) > 0)

    def test_check_assumptions_returns_dict(self):
        result = self.model.check_assumptions(print_conclusions=False)
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)
        self.assertIn("p-value", result["normality (Shapiro-Wilk)"])
        self.assertIn("Conclusion", result["homoscedasticity (Levene)"])

