# src/expdespy/models/splitplot_dbc.py

from expdespy.models.splitplot_base import SplitPlotDesign

class SplitPlotRCBD(SplitPlotDesign):
    """Plots subdivididas em DBC (com blocos)."""
    def _get_formula(self):
        return f"{self.response} ~ C({self.block}) + C({self.main_plot}) * C({self.subplot})"