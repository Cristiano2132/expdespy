"""
Módulo de modelos estatísticos para delineamentos experimentais.
Inclui implementações de DIC, DBC e a classe base ExperimentalDesign.
"""

from .dic import DIC
from .dbc import DBC
from .base import ExperimentalDesign

__all__ = ["DIC", "DBC", "ExperimentalDesign"]