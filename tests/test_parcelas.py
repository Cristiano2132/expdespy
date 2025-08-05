import unittest
import pandas as pd

from expdespy.datasets import load_splitplot_dic, load_splitplot_dbc
from expdespy.models import SplitPlotDIC, SplitPlotDBC

class TestSplitPlotDIC(unittest.TestCase):
    def setUp(self):
        self.df, self.desc = load_splitplot_dic()
        self.model = SplitPlotDIC(
            data=self.df,
            response=self.desc['response'],
            main_plot=self.desc['main_plot'],
            subplot=self.desc['subplot']
        )

    def test_anova_returns_dataframe(self):
        result = self.model.anova()
        self.assertIsInstance(result, pd.DataFrame)
        for col in ['PR(>F)', 'F']:
            self.assertIn(col, result.columns)

    def test_check_assumptions_returns_dict(self):
        result = self.model.check_assumptions(alpha=0.05, print_conclusions=False)
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)
        

class TestSplitPlotDBC(unittest.TestCase):
    def setUp(self):
        self.df, self.desc = load_splitplot_dbc()
        self.model = SplitPlotDBC(
            data=self.df,
            response=self.desc['response'],
            block=self.desc['block'],
            main_plot=self.desc['main_plot'],
            subplot=self.desc['subplot']
        )

    def test_anova_returns_dataframe(self):
        result = self.model.anova()
        self.assertIsInstance(result, pd.DataFrame)
        for col in ['PR(>F)', 'F']:
            self.assertIn(col, result.columns)

    def test_check_assumptions_returns_dict(self):
        result = self.model.check_assumptions(alpha=0.05, print_conclusions=False)
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)