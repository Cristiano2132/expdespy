# src/expdespy/models/fatorial_dbc.py

from expdespy.models.fatorial_base import FatorialDesign

class FactorialRCBD(FatorialDesign):
    def __init__(self, data, response, factors, block):
        self.block = block
        super().__init__(data, response, factors)

    def _get_formula(self):
        return f"{self.response} ~ {self.block} + " + "*".join([f"C({f})" for f in self.factors])