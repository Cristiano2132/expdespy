import unittest
import pandas as pd
import numpy as np
from expdespy import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        # Dataset para get_summary (mesmo número de linhas em todas as colunas)
        self.df = pd.DataFrame({
            "num": [1, 2, 2, 3, np.nan],
            "cat": ["A", "A", "B", "B", "B"],
            "many": [0, 1, 2, 3, 4]  # agora só 5 valores
        })

        # Dataset todo NaN
        self.df_nan = pd.DataFrame({
            "col": [np.nan] * 5
        })

        # Dataset para assign_letters
        self.df_posthoc = pd.DataFrame({
            "G1": ["A", "A", "B"],
            "G2": ["B", "C", "C"],
            "pval": [0.04, 0.2, 0.03]
        })

        self.data_original = pd.DataFrame({
            "grupo": ["A", "A", "B", "B", "C", "C"],
            "valor": [10, 12, 15, 16, 20, 19]
        })
    def test_get_summary_basic(self):
        summary = utils.get_summary(self.df)
        self.assertIn("num", summary.index)
        self.assertEqual(summary.loc["cat", "top_class"], "B")
        self.assertEqual(summary.loc["many", "unique_values"], summary.loc["many", "unique_values"])

    def test_get_summary_all_nan(self):
        summary_nan = utils.get_summary(self.df_nan)
        self.assertEqual(summary_nan.loc["col", "top_class"], "...")
        self.assertEqual(summary_nan.loc["col", "top_class_pct"], "...")

    def test_assign_letters_default_order(self):
        result = utils.assign_letters(self.df_posthoc, "G1", "G2", "pval")
        self.assertIn("A", result.index)
        self.assertTrue(all(isinstance(v, str) for v in result["Letters"]))

    def test_assign_letters_with_custom_order(self):
        result = utils.assign_letters(self.df_posthoc, "G1", "G2", "pval", order=["C", "B", "A"])
        self.assertEqual(list(result.index), ["C", "B", "A"])

    def test_assign_letters_with_order_ascending(self):
        result = utils.assign_letters(
            self.df_posthoc, "G1", "G2", "pval",
            order="ascending", data=self.data_original, vals="valor", group="grupo"
        )
        self.assertEqual(list(result.index), ["A", "B", "C"])  # menores médias primeiro

    def test_assign_letters_with_order_descending(self):
        result = utils.assign_letters(
            self.df_posthoc, "G1", "G2", "pval",
            order="descending", data=self.data_original, vals="valor", group="grupo"
        )
        self.assertEqual(list(result.index), ["C", "B", "A"])  # maiores médias primeiro

    def test_assign_letters_order_ascending_without_data_raises(self):
        with self.assertRaises(ValueError):
            utils.assign_letters(self.df_posthoc, "G1", "G2", "pval", order="ascending")

