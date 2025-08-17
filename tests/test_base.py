# tests/test_base.py

import unittest
import numpy as np
import pandas as pd
from expdespy.models.base import ExperimentalDesign


class DummyDesign(ExperimentalDesign):
    """
    Classe dummy para testar ExperimentalDesign
    """
    def _get_formula(self) -> str:
        return "y ~ C(trat)"


class TestExperimentalDesign(unittest.TestCase):

    def setUp(self):
        # Criar dataset com dois tratamentos e 5 repetições cada
        self.data = pd.DataFrame({
            "trat": np.repeat(["A", "B"], 5),
            "y": np.concatenate([
                np.random.normal(loc=10, scale=1.0, size=5),
                np.random.normal(loc=15, scale=1.0, size=5)
            ])
        })
        self.design = DummyDesign(self.data, response="y", treatment="trat")

    def test_anova_returns_dataframe_with_significance(self):
        # Act
        anova_table = self.design.anova()

        # Assert
        self.assertIsInstance(anova_table, pd.DataFrame)
        self.assertIn("Signif", anova_table.columns)
        self.assertTrue(all(sig in ["***", "**", "*", "ns", " "] for sig in anova_table["Signif"]))

    def test_check_assumptions_returns_dict(self):
        # Act
        result = self.design.check_assumptions(print_conclusions=False)

        # Assert
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)
        self.assertIn("p-value", result["normality (Shapiro-Wilk)"])
        self.assertIn("p-value", result["homoscedasticity (Levene)"])

    def test_anova_significance_marker_logic(self):
        """
        Testa se valores extremos de p produzem as marcações corretas
        """
        # Dados com diferença clara
        data = pd.DataFrame({
            "trat": np.repeat(["A", "B"], 10),
            "y": np.concatenate([
                np.ones(10) * 1,   # média baixa
                np.ones(10) * 10   # média alta
            ])
        })
        design = DummyDesign(data, response="y", treatment="trat")
        anova_table = design.anova()

        # Como a diferença é muito grande, o p-value deve ser muito pequeno
        p_val = anova_table.loc["C(trat)", "PR(>F)"]
        signif = anova_table.loc["C(trat)", "Signif"]

        self.assertLess(p_val, 0.001)
        self.assertEqual(signif, "***")

