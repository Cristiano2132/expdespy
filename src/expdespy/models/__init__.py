"""
Módulo de modelos estatísticos para delineamentos experimentais.
Inclui implementações de CRD, RCBD e a classe base ExperimentalDesign.
"""

from .dic import CRD
from .dbc import RCBD
from .dql import LSD
from .base import ExperimentalDesign
from .fatorial_base import FactorialDesign
from .fatorial_dic import FactorialCRD
from .fatorial_dbc import FactorialRCBD
from .splitplot_base import SplitPlotDesign
from .splitplot_dic import SplitPlotCRD
from .splitplot_dbc import SplitPlotRCBD

__all__ = ["CRD",
    "RCBD",
    "ExperimentalDesign",
    "LSD",
    "FactorialDesign",
    "FactorialCRD",
    "FactorialRCBD",
    "SplitPlotDesign",
    "SplitPlotCRD",
    "SplitPlotRCBD"
    ]
