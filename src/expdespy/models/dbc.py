from expdespy.models.base import ExperimentalDesign
import pandas as pd
from typing import Dict, Optional
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import scipy.stats as stats
import matplotlib.axes


class DBC(ExperimentalDesign):
    def __init__(self, data: pd.DataFrame, response: str, treatment: str, block: str):
        """
        Inicializa um modelo de DBC (Delineamento em Blocos Casualizados).

        Parameters:
            data: DataFrame com os dados experimentais
            response: Nome da variável resposta
            treatment: Nome da coluna de tratamentos
            block: Nome da coluna dos blocos
        """
        super().__init__(data, response, treatment)
        self.block = block

    def anova(self) -> pd.DataFrame:
        """
        Executa a análise de variância (ANOVA) para o delineamento DBC.

        Returns:
            DataFrame com a tabela ANOVA (Tipo II).
        """
        formula = f"{self.response} ~ C({self.treatment}) + C({self.block})"
        model = smf.ols(formula, data=self.data).fit()
        result = anova_lm(model, typ=2)
        return result

    def posthoc(self, method: str = "tukey") -> pd.DataFrame:
        """
        Realiza o teste de comparação múltipla após ANOVA.

        Parameters:
            method: Método de comparação múltipla (atualmente apenas "tukey" é suportado)

        Returns:
            DataFrame com os resultados do teste de Tukey.
        """
        if method.lower() != "tukey":
            raise NotImplementedError("Atualmente apenas o teste de Tukey é suportado.")

        tukey = pairwise_tukeyhsd(
            endog=self.data[self.response],
            groups=self.data[self.treatment],
            alpha=0.05
        )

        result_df = pd.DataFrame(data=tukey.summary().data[1:], columns=tukey.summary().data[0])
        return result_df

    def plot_means(self, ax: Optional[matplotlib.axes.Axes] = None) -> None:
        """
        Plota as médias por tratamento. Pode receber um Axes externo para composição.

        Parameters:
            ax: Um objeto matplotlib.axes.Axes. Se None, cria um novo gráfico.
        """
        means = self.data.groupby(self.treatment)[self.response].mean().reset_index()

        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))

        ax.bar(means[self.treatment], means[self.response], color="skyblue")
        ax.set_xlabel(self.treatment)
        ax.set_ylabel(f"Média de {self.response}")
        ax.set_title("Médias por tratamento (DBC)")
        ax.grid(True)

        if ax is None:
            plt.tight_layout()
            plt.show()

    def check_assumptions(self) -> Dict[str, bool]:
        """
        Verifica os pressupostos da ANOVA:
        - Normalidade dos resíduos (Shapiro-Wilk)
        - Homocedasticidade (teste de Levene)

        Returns:
            Dict com o resultado de cada verificação (True se o pressuposto for aceito).
        """
        formula = f"{self.response} ~ C({self.treatment}) + C({self.block})"
        model = smf.ols(formula, data=self.data).fit()
        residuals = model.resid

        normality_p = stats.shapiro(residuals).pvalue
        is_normal = normality_p > 0.05

        groups = [group[self.response].values for _, group in self.data.groupby(self.treatment)]
        levene_p = stats.levene(*groups).pvalue
        is_homoscedastic = levene_p > 0.05

        return {
            "normality (Shapiro-Wilk)": is_normal,
            "homoscedasticity (Levene)": is_homoscedastic
        }