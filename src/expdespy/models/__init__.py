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
from .splitplot_base import SplitPlotDesign
from .splitplot_dic import SplitPlotDIC
from .splitplot_dbc import SplitPlotDBC

__all__ = ["DIC",
    "DBC",
    "ExperimentalDesign",
    "DQL",
    "FatorialDesign",
    "FatorialDIC",
    "FatorialDBC",
    "SplitPlotDesign",
    "SplitPlotDIC",
    "SplitPlotDBC"
    ]
