from expdespy.models.base import ExperimentalDesign
import pandas as pd


class DQL(ExperimentalDesign):
    def __init__(self, data: pd.DataFrame, response: str, treatment: str, block_row: str, block_col: str):
        super().__init__(data, response, treatment)
        self.block_row = block_row
        self.block_col = block_col

    def _get_formula(self) -> str:
        return f"{self.response} ~ C({self.treatment}) + C({self.block_row}) + C({self.block_col})"
