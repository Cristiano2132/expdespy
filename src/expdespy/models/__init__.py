"""
Módulo de modelos estatísticos para delineamentos experimentais.
Inclui implementações de DIC, DBC e a classe base ExperimentalDesign.
"""

from .dic import DIC
from .dbc import DBC
from .dql import DQL
from .base import ExperimentalDesign
from .fatorial_base import FatorialDesign
from .fatorial_dic import FatorialDIC
from .fatorial_dbc import FatorialDBC

__all__ = ["DIC",
    "DBC",
    "ExperimentalDesign",
    "DQL",
    "FatorialDesign",
    "FatorialDIC",
    "FatorialDBC"
    ]
