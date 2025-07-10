import unittest
import pandas as pd

from expdespy.datasets import load_fatorial_rcbd_np
from expdespy.models import FatorialDBC
from statsmodels.stats.anova import anova_lm

class TestFatorialRCBD(unittest.TestCase):
    def setUp(self):
        self.df, self.desc = load_fatorial_rcbd_np()
        self.model = FatorialDBC(
            data=self.df,
            response=self.desc['response'],
            factors=self.desc['factors'],
            block=self.desc['blocks']
        )

    def test_anova_returns_dataframe(self):
        result = self.model.anova()
        self.assertIsInstance(result, pd.DataFrame)
        for col in ['PR(>F)', 'F']:
            self.assertIn(col, result.columns)

        f_np_esperado = 4.696
        # Teste do valor de F do termo de interação N:P
        f_np = float(result.loc["C(N):C(P)", "F"])
        self.assertAlmostEqual(f_np, f_np_esperado, places=2)

    def test_check_assumptions_returns_dict(self):
        result = self.model.check_assumptions(alpha=0.05, print_conclusions=False)
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)