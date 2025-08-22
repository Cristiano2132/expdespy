import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

class PolynomialRegression:
    """
    Fits polynomial models for quantitative treatments.
    """
    def __init__(self, data: pd.DataFrame, response: str, treatment: str):
        self.data = data.copy()
        self.response = response
        self.treatment = treatment
        self.model = None
        self.results = None

    def fit(self, degree: int = 1) -> sm.regression.linear_model.RegressionResultsWrapper:
        """
        Fits a polynomial model of the specified degree.
        
        Args:
            degree (int): Degree of the polynomial to fit.

        Returns:
            sm.regression.linear_model.RegressionResultsWrapper: Results of the fitted model.
        """
        if degree < 1:
            raise ValueError("The polynomial degree must be at least 1.")

        # Create polynomial terms
        for d in range(2, degree + 1):
            self.data[f"{self.treatment}^{d}"] = self.data[self.treatment] ** d

        # Create model formula
        predictors = [f"Q('{self.treatment}')" ] + [f"Q('{self.treatment}^{d}')" for d in range(2, degree + 1)]
        formula = f"Q('{self.response}') ~ {' + '.join(predictors)}"

        # Fit model
        self.model = smf.ols(formula=formula, data=self.data)
        self.results = self.model.fit()
        return self.results

    def anova(self) -> pd.DataFrame:
        """
        Returns the ANOVA of the fitted model.

        Returns:
            pd.DataFrame: ANOVA results.
        """
        if self.results is None:
            raise ValueError("Model not fitted. Use .fit() first.")
        return sm.stats.anova_lm(self.results)

    def plot(self, ax: plt.Axes = None):
        """
        Plots the observed points and the fitted curve.

        Args:
            ax (plt.Axes, optional): Axes on which to plot. If None, creates new axes.

        Returns:
            plt.Axes: Axes on which the plot was drawn.
        """
        if ax is None:
            _, ax = plt.subplots(figsize=(8, 5))
        if self.results is None:
            raise ValueError("Model not fitted. Use .fit() first.")

        # Generate values for prediction
        x_vals = np.linspace(self.data[self.treatment].min(),
                            self.data[self.treatment].max(), 100)
        X_pred = pd.DataFrame({self.treatment: x_vals})

        # Add polynomial terms
        for d in range(2, len(self.results.params)):
            X_pred[f"{self.treatment}^{d}"] = X_pred[self.treatment] ** d

        # Predict values
        y_pred = self.results.predict(X_pred)

        # Plot observed data and fitted curve
        ax.scatter(self.data[self.treatment], self.data[self.response], color="blue", label="Data")
        ax.plot(x_vals, y_pred, color="red", label=f"Polynomial fit (degree {len(self.results.params)-1})")
        ax.set_xlabel(self.treatment)
        ax.set_ylabel(self.response)
        ax.legend()
        return ax

# if __name__ == "__main__":

#     # Example data (quantitative treatment)
#     df = pd.DataFrame({
#         "dose": [0, 1, 2, 3, 4, 5],
#         "yield": [5, 7, 9, 15, 18, 20]
#     })

#     # Fit quadratic model
#     reg = PolynomialRegression(df, response="yield", treatment="dose")
#     results = reg.fit(degree=2)

#     # ANOVA
#     print(reg.anova())

#     # Model summary
#     print(results.summary())

#     # Plot
#     fig, ax = plt.subplots()
#     reg.plot(ax=ax)
#     plt.show()