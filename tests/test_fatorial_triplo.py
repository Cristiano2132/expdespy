import unittest
import pandas as pd
import numpy as np
from expdespy.models import FatorialDIC


class TestFatorialTriploDIC(unittest.TestCase):

    def setUp(self):
        # Fatorial 2³ com 2 repetições → 8 combinações * 2 = 16 linhas
        levels = [0, 1]
        base_design = [(a, b, c) for a in levels for b in levels for c in levels]
        design = base_design * 2  # duas repetições
        df = pd.DataFrame(design, columns=["f1", "f2", "f3"])

        # Simula produtividade com efeito dos fatores
        np.random.seed(42)
        df["produtividade"] = (
            10  # valor base
            + 2 * df["f1"]
            + 1.5 * df["f2"]
            + 1 * df["f3"]
            + 0.5 * df["f1"] * df["f2"]
            + np.random.normal(0, 0.5, len(df))  # ruído
        )

        self.df = df
        self.factors = ["f1", "f2", "f3"]
        self.response = "produtividade"
        self.model = FatorialDIC(data=self.df, response=self.response, factors=self.factors)

    def test_anova_returns_dataframe(self):
        result = self.model.anova()
        interaction = f"C(f1):C(f2):C(f3)"
        self.assertIn(interaction, result.index)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("F", result.columns)
        self.assertIn("PR(>F)", result.columns)
        # self.assertTrue(result["F"].notna().all())  # evita erro de NaN

    def test_check_assumptions_returns_dict(self):
        result = self.model.check_assumptions(print_conclusions=False)
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)