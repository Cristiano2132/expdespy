import unittest
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

from expdespy.datasets.dic_milho import load_dic_milho
from expdespy.posthoc.lsd_test import LSDTest


class TestLSDTest(unittest.TestCase):

    def setUp(self):
        self.df, _ = load_dic_milho()

        # Fit ANOVA to extract MSE and df_resid
        model = ols("produtividade ~ C(variedade)", data=self.df).fit()
        anova_table = anova_lm(model, typ=2)

        # LSD clássico (t-test)
        self.lsd_t = LSDTest(
            self.df,
            values_column="produtividade",
            treatments_column="variedade",
            anova_table=anova_table,
            method="t"
        )

        # LSD baseado em Tukey
        self.lsd_tukey = LSDTest(
            self.df,
            values_column="produtividade",
            treatments_column="variedade",
            anova_table=anova_table,
            method="tukey"
        )

    def test_run_returns_dataframe(self):
        for lsd in [self.lsd_t, self.lsd_tukey]:
            result = lsd.run()
            self.assertIsInstance(result, pd.DataFrame)
            self.assertIn("group1", result.columns)
            self.assertIn("group2", result.columns)
            self.assertIn("p-value", result.columns)

    def test_cld_returns_dataframe(self):
        for lsd in [self.lsd_t, self.lsd_tukey]:
            cld = lsd.run_compact_letters_display()
            self.assertIsInstance(cld, pd.DataFrame)
            self.assertIn("Letters", cld.columns)

    def test_plot_runs(self):
        for lsd in [self.lsd_t, self.lsd_tukey]:
            fig, ax = plt.subplots()
            try:
                lsd.plot_compact_letters_display(ax=ax)
            except Exception as e:
                self.fail(f"LSDTest ({lsd.method}) plot raised {e}")

    def test_cld_expected_letters_tukey(self):
        """Check if LSD (tukey method) assigns expected significance letters to groups"""
        cld = self.lsd_tukey.run_compact_letters_display()

        expected_letters = {
            "D": "a",
            "B": "ab",
            "C": "b",
            "A": "b"
        }

        actual_letters = cld.set_index("variedade")["Letters"].to_dict()

        for group, expected in expected_letters.items():
            self.assertEqual(
                actual_letters[group],
                expected,
                msg=f"Group {group} expected letter {expected}, got {actual_letters[group]}"
            )

    def test_cld_expected_letters_t(self):
        """Check if LSD (t method) assigns expected significance letters to groups"""
        cld = self.lsd_t.run_compact_letters_display()

        expected_letters = {
            "D": "a",
            "B": "b",
            "C": "bc",
            "A": "c"
        }

        actual_letters = cld.set_index("variedade")["Letters"].to_dict()

        for group, expected in expected_letters.items():
            self.assertEqual(
                actual_letters[group],
                expected,
                msg=f"Group {group} expected letter {expected}, got {actual_letters[group]}"
            )