# src/expdespy/models/base.py

from abc import ABC, abstractmethod
from typing import Dict, Optional

import matplotlib.axes
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd


class ExperimentalDesign(ABC):
    """
    Classe base abstrata para delineamentos experimentais.

    Esta classe provê métodos comuns para análise estatística,
    como ANOVA, verificação de pressupostos, testes post hoc e
    visualização de médias.

    Cada delineamento específico deve herdar desta classe e
    implementar o método abstrato `_get_formula`, que retorna
    a fórmula estatística usada na modelagem.

    Attributes:
        data (pd.DataFrame): Dados do experimento.
        response (str): Nome da variável resposta.
        treatment (str): Nome da coluna dos tratamentos.
    """

    def __init__(self, data: pd.DataFrame, response: str, treatment: str):
        self.data = data
        self.response = response
        self.treatment = treatment

    @abstractmethod
    def _get_formula(self) -> str:
        """
        Retorna a fórmula do modelo estatístico (string).

        Deve ser sobrescrita por cada subclasse para refletir o
        delineamento específico.

        Returns:
            str: Fórmula para análise estatística.
        """
        pass

    def anova(self) -> pd.DataFrame:
        """
        Realiza a análise de variância (ANOVA) usando a fórmula
        definida pelo método `_get_formula`.

        Returns:
            pd.DataFrame: Tabela ANOVA do modelo ajustado (Tipo II).
        """
        formula = self._get_formula()
        model = smf.ols(formula, data=self.data).fit()

        def significance_marker(p):
            if p < 0.001:
                return "***"
            elif p < 0.01:
                return "**"
            elif p < 0.05:
                return "*"
            elif np.isnan(p):
                return " "
            else:
                return "ns"

        anova_table = anova_lm(model, typ=2)
        # Criar nova coluna com os símbolos
        anova_table["Signif"] = anova_table["PR(>F)"].apply(significance_marker)

        return anova_table

    def check_assumptions(self, alpha: float = 0.05) -> Dict[str, bool]:
        """
        Verifica os pressupostos da ANOVA:
        - Normalidade dos resíduos (teste Shapiro-Wilk)
        - Homocedasticidade (teste de Levene)

        Args:
            alpha (float, optional): Nível de significância. Padrão é 0.05.
        Returns:
            Dict[str, bool]: Dicionário com o resultado dos testes,
            True indica que o pressuposto foi atendido.
        """
        formula = self._get_formula()
        model = smf.ols(formula, data=self.data).fit()
        residuals = model.resid

        normality_p = stats.shapiro(residuals).pvalue
        is_normal = normality_p > alpha

        groups = [
            group[self.response].values
            for _, group in self.data.groupby(self.treatment)
        ]
        levene_p = stats.levene(*groups).pvalue
        is_homoscedastic = levene_p > alpha
        print(f"""
            Normality (Shapiro-Wilk): 
                - H0: The residuals are normally distributed
                - H1: The residuals are not normally distributed
            - p-value: {normality_p}
            Conclusion: H0 must {"not be rejected" if is_normal else "be rejected"}
            Homoscedasticity (Levene):
                - H0: The variances of the groups are equal
                - H1: The variances of the groups are not equal
            - p-value: {levene_p}
            Conclusion: H0 must {"not be rejected" if is_homoscedastic else "be rejected"}
            """
        )

        return {
            "normality (Shapiro-Wilk)": is_normal,
            "homoscedasticity (Levene)": is_homoscedastic,
        }

    def posthoc(self, method: str = "tukey") -> pd.DataFrame:
        """
        Realiza teste post hoc para comparações múltiplas após ANOVA.

        Atualmente, apenas o teste de Tukey é suportado.

        Args:
            method (str): Nome do método post hoc (default: "tukey").

        Returns:
            pd.DataFrame: Resultados do teste post hoc.
        """
        if method.lower() != "tukey":
            raise NotImplementedError("Atualmente apenas o teste de Tukey é suportado.")
        tukey = pairwise_tukeyhsd(
            endog=self.data[self.response], groups=self.data[self.treatment], alpha=0.05
        )
        return pd.DataFrame(tukey.summary().data[1:], columns=tukey.summary().data[0])

    def plot_means(self, ax: Optional[matplotlib.axes.Axes] = None) -> None:
        """
        Plota as médias da variável resposta agrupadas por tratamento.

        Args:
            ax (Optional[matplotlib.axes.Axes]): Eixo matplotlib para plotagem.
                Se None, cria uma nova figura e eixo.
        """
        means = self.data.groupby(self.treatment)[self.response].mean().reset_index()
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(means[self.treatment], means[self.response], color="skyblue")
        ax.set_xlabel(self.treatment)
        ax.set_ylabel(f"Média de {self.response}")
        ax.set_title("Médias por tratamento")
        ax.grid(True)
        if ax is None:
            plt.tight_layout()
            plt.show()
