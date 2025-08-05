# src/expdespy/models/splitplot_base.py

from abc import ABC, abstractmethod
from expdespy.models.base import ExperimentalDesign

class SplitPlotDesign(ExperimentalDesign, ABC):
    def __init__(self, data, response: str, main_plot: str, subplot: str, block: str = None):
        self.main_plot = main_plot
        self.subplot = subplot
        self.block = block
        treatment_formula = f"C({main_plot}) * C({subplot})"
        super().__init__(data, response, treatment_formula)

    @abstractmethod
    def _get_formula(self) -> str:
        pass