import unittest
import pandas as pd
from expdespy.posthoc.posthoc_loader import PostHocLoader
from expdespy.posthoc import TukeyHSD, PairwiseTTest 

class TestPostHocLoader(unittest.TestCase):

    def setUp(self):
        # Dados de exemplo
        self.df = pd.DataFrame({
            'trat': ['A', 'A', 'B', 'B', 'C', 'C'],
            'resp': [10, 12, 15, 14, 13, 16]
        })
        self.alpha = 0.05
        self.values_column = 'resp'
        self.trats_column = 'trat'

    def test_create_tukey(self):
        test_instance = PostHocLoader.create(
            test_name='tukey',
            data=self.df,
            values_column=self.values_column,
            trats_column=self.trats_column,
            alpha=self.alpha
        )
        self.assertIsInstance(test_instance, TukeyHSD)

    def test_create_ttest(self):
        test_instance = PostHocLoader.create(
            test_name='ttest',
            data=self.df,
            values_column=self.values_column,
            trats_column=self.trats_column,
            alpha=self.alpha
        )
        self.assertIsInstance(test_instance, PairwiseTTest)

    def test_invalid_test_name_raises_error(self):
        with self.assertRaises(ValueError) as context:
            PostHocLoader.create(
                test_name='invalid',
                data=self.df,
                values_column=self.values_column,
                trats_column=self.trats_column,
                alpha=self.alpha
            )
        self.assertIn("não é suportado", str(context.exception))
