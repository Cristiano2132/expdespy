from expdespy.models.base import ExperimentalDesign
import pandas as pd

class DBC(ExperimentalDesign):
    def __init__(self, data: pd.DataFrame, response: str, treatment: str, block: str):
        super().__init__(data, response, treatment)
        self.block = block

    def _get_formula(self) -> str:
        return f"{self.response} ~ C({self.treatment}) + C({self.block})"