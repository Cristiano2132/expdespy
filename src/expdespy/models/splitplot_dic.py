# src/expdespy/models/splitplot_dic.py

from expdespy.models.splitplot_base import SplitPlotDesign

class SplitPlotCRD(SplitPlotDesign):
    def _get_formula(self):
        return f"{self.response} ~ C({self.main_plot}) * C({self.subplot})"