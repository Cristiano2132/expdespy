import unittest
import pandas as pd
import matplotlib.pyplot as plt

from expdespy.posthoc.base import PostHocTest


class MockPostHoc(PostHocTest):
    """Mock implementation for testing the abstract PostHocTest."""

    def run(self) -> pd.DataFrame:
        return pd.DataFrame({
            "group1": ["A", "B"],
            "group2": ["B", "C"],
            "p-value": [0.01, 0.20]
        })

    def _pvalue_column_name(self) -> str:
        return "p-value"


class TestPostHocBase(unittest.TestCase):

    def setUp(self):
        df = pd.DataFrame({
            "group": ["A", "A", "B", "B", "C", "C"],
            "value": [10, 12, 15, 14, 20, 21]
        })
        self.posthoc = MockPostHoc(
            df, values_column="value", treatments_column="group"
        )

    def test_run_returns_dataframe(self):
        result = self.posthoc.run()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("group1", result.columns)
        self.assertIn("group2", result.columns)

    def test_cld_returns_dataframe(self):
        cld = self.posthoc.run_compact_letters_display()
        self.assertIsInstance(cld, pd.DataFrame)
        self.assertIn("Letters", cld.columns)

    def test_plot_runs(self):
        fig, ax = plt.subplots()
        try:
            self.posthoc.plot_compact_letters_display(ax=ax)
        except Exception as e:
            self.fail(f"plot_compact_letters_display() raised {e}")