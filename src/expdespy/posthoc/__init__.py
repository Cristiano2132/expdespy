"""
expdespy.posthoc
================

This subpackage provides implementations of common **post hoc tests** used in
experimental design analysis. Post hoc tests are statistical procedures
performed after an ANOVA when significant differences are detected, in order
to identify which specific treatment groups differ from each other.

Implemented tests
-----------------
- **PairwiseTTest**: Uncorrected pairwise t-tests between treatment groups.
- **TukeyHSD**: Tukey's Honest Significant Difference test for multiple comparisons.
- **LSDTest**: Fisher’s Least Significant Difference test, requiring residual
  mean square (MSE) and residual degrees of freedom from the ANOVA.

All tests inherit from the abstract base class **PostHocTest**, which defines
the common interface for running tests, extracting results, and producing
compact letter displays (CLD).

Visualization
-------------
The `plots` module provides additional tools for visualizing post hoc test
results:
- **plot_boxplot_with_letters**: Enhanced boxplot with treatment means,
  optional hue, and significance letters.
- **plot_significance_heatmap**: Heatmap of pairwise comparison significance
  levels, with intuitive coloring for 1%, 5%, and 10% thresholds.

Example
-------
>>> from expdespy.posthoc import TukeyHSD, plot_boxplot_with_letters
>>> from expdespy.datasets import load_dic_milho
>>> data, _ = load_dic_milho()
>>> tukey = TukeyHSD(data, values_column="produtividade", treatments_column="variedade")
>>> results = tukey.run()
>>> cld = tukey.run_compact_letters_display()
>>> plot_boxplot_with_letters(data, cld, values_column="produtividade", treatments_column="variedade")
"""

from expdespy.posthoc.base import PostHocTest
from expdespy.posthoc.t_test import PairwiseTTest
from expdespy.posthoc.tukey_test import TukeyHSD
from expdespy.posthoc.lsd_test import LSDTest
from expdespy.posthoc.plots import (
    plot_boxplot_with_letters,
    plot_significance_heatmap,
)

__all__ = [
    # Base
    "PostHocTest",
    # Tests
    "PairwiseTTest",
    "TukeyHSD",
    "LSDTest",
    # Visualization
    "plot_boxplot_with_letters",
    "plot_significance_heatmap",
]