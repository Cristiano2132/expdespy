# src/expdespy/models/fatorial_dic.py

from expdespy.models.fatorial_base import FatorialDesign

class FactorialCRD(FatorialDesign):
    """Modelo fatorial em DIC."""

    def _get_formula(self):
        return f"{self.response} ~ " + "*".join([f"C({f})" for f in self.factors])
