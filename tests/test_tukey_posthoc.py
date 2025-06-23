import unittest
import pandas as pd
import matplotlib.pyplot as plt

from expdespy.datasets.dic_milho import load_dic_milho
from expdespy.posthoc.tukey_test import TukeyHSD


class TestTukeyHSD(unittest.TestCase):

    def setUp(self):
        self.df, _ = load_dic_milho()
        self.tukey = TukeyHSD(
            self.df, values_column='produtividade', trats_column='variedade')

    def test_run_returns_dataframe(self):
        result = self.tukey.run()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('group1', result.columns)
        self.assertIn('group2', result.columns)
        self.assertIn('p-adj', result.columns)

    def test_cld_returns_dataframe(self):
        cld = self.tukey.run_compact_letters_display()
        self.assertIsInstance(cld, pd.DataFrame)
        self.assertIn('Letters', cld.columns)

    def test_plot_runs(self):
        fig, ax = plt.subplots()
        try:
            self.tukey.plot_compact_letters_display(ax=ax)
        except Exception as e:
            self.fail(
                f"Tukey plot_compact_letters_display() raised an exception: {e}")

    def test_cld_expected_letters(self):
        cld = self.tukey.run_compact_letters_display()
        expected_letters = {
            'D': 'a',
            'B': 'ab',
            'C': 'b',
            'A': 'b'
        }
        actual_letters = cld.set_index('variedade')['Letters'].to_dict()
        for group, expected in expected_letters.items():
            self.assertEqual(
                actual_letters[group],
                expected,
                msg=f"Letra para o grupo {group} esperada: {expected}, obtida: {actual_letters[group]}"
            )
