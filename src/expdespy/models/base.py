# src/expdespy/models/base.py

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict

class ExperimentalDesign(ABC):
    def __init__(self, data: pd.DataFrame, response: str, treatment: str):
        self.data = data
        self.response = response
        self.treatment = treatment

    @abstractmethod
    def anova(self) -> pd.DataFrame:
        """Run ANOVA and return result table."""
        pass

    @abstractmethod
    def posthoc(self, method: str = "tukey") -> pd.DataFrame:
        """Perform post-hoc test."""
        pass

    @abstractmethod
    def plot_means(self) -> None:
        """Plot means with significance letters."""
        pass

    @abstractmethod
    def check_assumptions(self) -> Dict[str, bool]:
        """Check ANOVA assumptions like normality and homogeneity of variances."""
        pass