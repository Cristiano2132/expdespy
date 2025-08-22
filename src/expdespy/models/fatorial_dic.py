# src/expdespy/models/fatorial_dic.py

from expdespy.models.fatorial_base import FactorialDesign

class FactorialCRD(FactorialDesign):

    def _get_formula(self):
        return f"{self.response} ~ " + "*".join([f"C({f})" for f in self.factors])
