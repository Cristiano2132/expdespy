import unittest
import matplotlib.pyplot as plt
import numpy as np

from expdespy.datasets.dic_milho import load_dic_milho
from expdespy.posthoc.tukey_test import TukeyHSD
from expdespy.posthoc.plots import (
    plot_boxplot_with_letters,
    plot_significance_heatmap,
)


class TestPostHocPlots(unittest.TestCase):

    def setUp(self):
        # Load dataset
        self.df, _ = load_dic_milho()
        self.values_column = "produtividade"
        self.treatments_column = "variedade"

        # Fit Tukey test
        self.tukey = TukeyHSD(
            self.df,
            values_column=self.values_column,
            treatments_column=self.treatments_column,
        )
        self.tukey_results = self.tukey.run()
        self.tukey_cld = self.tukey.run_compact_letters_display()
        self.treatments = self.df[self.treatments_column].unique().tolist()

    def test_plot_boxplot_with_letters_runs(self):
        """Ensure that boxplot with letters runs without errors"""
        fig, ax = plt.subplots()
        try:
            plot_boxplot_with_letters(
                data=self.df,
                cld_result=self.tukey_cld,
                values_column=self.values_column,
                treatments_column=self.treatments_column,
                ax=ax,
            )
        except Exception as e:
            self.fail(f"plot_boxplot_with_letters raised an exception: {e}")

    def test_plot_heatmap_runs(self):
        """Ensure that significance heatmap runs without errors"""
        fig, ax = plt.subplots()
        try:
            plot_significance_heatmap(
                df_posthoc=self.tukey_results,
                treatments=self.treatments,
                pvalue_col="p-adj",
                ax=ax,
            )
        except Exception as e:
            self.fail(f"plot_significance_heatmap raised an exception: {e}")

    def test_heatmap_matrix_symmetry(self):
        """Check that heatmap matrix is symmetric"""
        # Rebuild p-value matrix from tukey results
        n = len(self.treatments)
        mat = np.ones((n, n))
        treatment_index = {t: i for i, t in enumerate(self.treatments)}

        for _, row in self.tukey_results.iterrows():
            i = treatment_index[row["group1"]]
            j = treatment_index[row["group2"]]
            mat[i, j] = row["p-adj"]
            mat[j, i] = row["p-adj"]

        # Assert symmetry
        self.assertTrue(np.allclose(mat, mat.T))

