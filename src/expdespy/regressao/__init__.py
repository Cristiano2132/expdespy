# src/expdespy/regression/__init__.py

"""
Módulo de Regressão do pacote expdespy.

Inclui funcionalidades para:
- Ajuste polinomial para tratamentos quantitativos
- Diagnóstico de resíduos e testes estatísticos
- Funções de visualização e gráficos relacionados a modelos de regressão
"""

from .polynomial import PolynomialRegression
from .diagnostics import (
    plot_residuals_vs_fitted,
    qq_plot_residuals,
    plot_residual_hist,
    cooks_distance_plot,
    shapiro_test,
    breusch_pagan_test,
    durbin_watson_test,
)

__all__ = [
    # polynomial.py
    "PolynomialRegression",

    # diagnostics.py
    "plot_residuals_vs_fitted",
    "qq_plot_residuals",
    "plot_residual_hist",
    "cooks_distance_plot",
    "shapiro_test",
    "breusch_pagan_test",
    "durbin_watson_test",
]