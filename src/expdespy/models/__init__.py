"""
Módulo de modelos estatísticos para delineamentos experimentais.
Inclui implementações de DIC, DBC e a classe base ExperimentalDesign.
"""

from .dic import DIC
from .dbc import DBC
from .dql import DQL
from .base import ExperimentalDesign
from .fatorial_base import FatorialDesign
from .fatorial_dic import FactorialCRD
from .fatorial_dbc import FactorialRCBD
from .splitplot_base import SplitPlotDesign
from .splitplot_dic import SplitPlotCRD
from .splitplot_dbc import SplitPlotRCBD

__all__ = ["DIC",
    "DBC",
    "ExperimentalDesign",
    "DQL",
    "FatorialDesign",
    "FactorialCRD",
    "FactorialRCBD",
    "SplitPlotDesign",
    "SplitPlotCRD",
    "SplitPlotRCBD"
    ]
