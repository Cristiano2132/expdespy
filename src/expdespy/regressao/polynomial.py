import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

class PolynomialRegression:
    """
    Ajuste de modelos polinomiais para tratamentos quantitativos.
    """
    def __init__(self, data: pd.DataFrame, response: str, treatment: str):
        self.data = data.copy()
        self.response = response
        self.treatment = treatment
        self.model = None
        self.results = None

    def fit(self, degree: int = 1) -> sm.regression.linear_model.RegressionResultsWrapper:
        """
        Ajusta um modelo polinomial de grau especificado.
        Args:
            degree (int): Grau do polinômio a ser ajustado.

        Returns:
            sm.regression.linear_model.RegressionResultsWrapper: Resultados do modelo ajustado.
        """
        if degree < 1:
            raise ValueError("O grau do polinômio deve ser pelo menos 1.")

        # Criar termos polinomiais
        for d in range(2, degree + 1):
            self.data[f"{self.treatment}^{d}"] = self.data[self.treatment] ** d

        # Criar fórmula do modelo
        predictors = [f"Q('{self.treatment}')" ] + [f"Q('{self.treatment}^{d}')" for d in range(2, degree + 1)]
        formula = f"Q('{self.response}') ~ {' + '.join(predictors)}"

        # Ajustar modelo
        self.model = smf.ols(formula=formula, data=self.data)
        self.results = self.model.fit()
        return self.results

    def anova(self) -> pd.DataFrame:
        """
        Retorna a ANOVA do modelo ajustado.
        Returns:
            pd.DataFrame: Resultados da ANOVA.
        """
        if self.results is None:
            raise ValueError("Modelo não ajustado. Use .fit() antes.")
        return sm.stats.anova_lm(self.results)

    def plot(self, ax: plt.Axes = None):
        """
        Plota os pontos observados e a curva ajustada.
        Args:
            ax (plt.Axes, optional): Eixos em que plotar. Se None, cria novos eixos.

        Returns:
            plt.Axes: Eixos em que o gráfico foi plotado.
        """
        if ax is None:
            _, ax = plt.subplots(figsize=(8, 5))
        if self.results is None:
            raise ValueError("Modelo não ajustado. Use .fit() antes.")

        x_vals = np.linspace(self.data[self.treatment].min(),
                            self.data[self.treatment].max(), 100)
        X_pred = pd.DataFrame({self.treatment: x_vals})

        for d in range(2, len(self.results.params)):
            X_pred[f"{self.treatment}^{d}"] = X_pred[self.treatment] ** d

        y_pred = self.results.predict(X_pred)

        ax.scatter(self.data[self.treatment], self.data[self.response], color="blue", label="Dados")
        ax.plot(x_vals, y_pred, color="red", label=f"Ajuste polinomial (grau {len(self.results.params)-1})")
        ax.set_xlabel(self.treatment)
        ax.set_ylabel(self.response)
        ax.legend()
        return ax

# if __name__ == "__main__":

#     # Exemplo de dados (tratamento quantitativo)
#     df = pd.DataFrame({
#         "dose": [0, 1, 2, 3, 4, 5],
#         "yield": [5, 7, 9, 15, 18, 20]
#     })

#     # Ajuste de modelo quadrático
#     reg = PolynomialRegression(df, response="yield", treatment="dose")
#     results = reg.fit(degree=2)

#     # ANOVA
#     print(reg.anova())

#     # Resumo do modelo
#     print(results.summary())

#     # Plot
#     fig, ax = plt.subplots()
#     reg.plot(ax=ax)
#     plt.show()
