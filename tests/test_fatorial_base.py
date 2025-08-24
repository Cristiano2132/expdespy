import unittest
import pandas as pd
from expdespy.models.fatorial_base import FactorialDesign


class DummyFatorialDesign(FactorialDesign):
    """Classe auxiliar para testar FactorialDesign com fórmula no padrão real (C(...))."""
    def _get_formula(self):
        # Usa C(...) como no FactorialDesign original
        return f"{self.response} ~ " + "*".join([f"C({f})" for f in self.factors])


class TestFatorialDesign(unittest.TestCase):

    def setUp(self):
        # Dados simples sem interação significativa
        self.data = pd.DataFrame({
            "f1": ["A", "A", "A", "A", "B", "B", "B", "B"],
            "f2": ["X", "X", "Y", "Y", "X", "X", "Y", "Y"],
            "y": [10, 11, 12, 13, 15, 16, 18, 19]
        })
        self.model = DummyFatorialDesign(
            data=self.data,
            response="y",
            factors=["f1", "f2"]
        )

        # Dados com interação significativa
        self.data_interaction = pd.DataFrame({
            "f1": ["A", "A", "B", "B"] * 4,
            "f2": ["X", "Y", "X", "Y"] * 4,
            "y": [10, 15, 12, 30, 9, 14, 11, 29,
                  10, 15, 13, 31, 8, 16, 12, 28]
        })
        self.model_interaction = DummyFatorialDesign(
            data=self.data_interaction,
            response="y",
            factors=["f1", "f2"]
        )

    def test_formula_generation(self):
        expected_formula = "y ~ C(f1)*C(f2)"
        self.assertEqual(self.model._get_formula(), expected_formula)

    def test_anova_returns_dataframe(self):
        result = self.model.run_anova()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("PR(>F)", result.columns)

    def test_check_assumptions_returns_dict(self):
        result = self.model.check_assumptions(print_conclusions=False)
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)

    def test_run_anova_with_max_interaction(self):
        result = self.model.run_anova(max_interaction=1)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("Signif", result.columns)

    def test_unfold_interactions_without_significant_interaction(self):
        results = self.model.unfold_interactions(print_results=False)
        self.assertIn("anova", results)
        self.assertTrue("main_effects" in results or "interactions" in results)

    def test_unfold_interactions_with_significant_interaction(self):
        results = self.model_interaction.unfold_interactions(print_results=False)
        self.assertIn("anova", results)
        self.assertTrue("interactions" in results or "main_effects" in results)

    def test_display_unfolded_interactions(self):
        results = self.model.unfold_interactions(print_results=False)
        # Apenas verifica se a função roda sem erros
        self.model.display_unfolded_interactions(results)


class TestFatorialDesignExtra(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            "C": ["A", "B"] * 4,
            "f2": ["X", "Y"] * 4,
            "y": [10, 12, 14, 16, 11, 13, 15, 17]
        })
        self.model_reserved = DummyFatorialDesign(
            data=self.data.copy(),
            response="y",
            factors=["C", "f2"]
        )

        self.data_interaction = pd.DataFrame({
            "f1": ["A", "A", "B", "B"] * 4,
            "f2": ["X", "Y", "X", "Y"] * 4,
            "y": [10, 25, 12, 30, 9, 26, 11, 29,
                10, 27, 13, 31, 8, 28, 12, 32]
        })
        self.model_interaction = DummyFatorialDesign(
            data=self.data_interaction,
            response="y",
            factors=["f1", "f2"]
        )

    def test_safe_factor_reserved_name(self):
        self.assertIn("C_", self.model_reserved.data.columns)

    def test_check_assumptions_prints(self):
        result = self.model_reserved.check_assumptions(print_conclusions=True)
        self.assertIn("normality (Shapiro-Wilk)", result)

    def test_run_anova_with_and_without_max_interaction(self):
        df1 = self.model_reserved.run_anova(max_interaction=1)
        df2 = self.model_reserved.run_anova(max_interaction=None)
        self.assertIn("Signif", df1.columns)
        self.assertIn("Signif", df2.columns)

    def test_unfold_interactions_with_exception_in_posthoc(self):
        bad_model = DummyFatorialDesign(
            data=self.data.rename(columns={"f2": "missing"}),
            response="y",
            factors=["C", "missing"]
        )
        results = bad_model.unfold_interactions(print_results=False)
        self.assertIn("anova", results)

    def test_display_with_non_dataframe_anova(self):
        results = {"anova": "texto simples"}
        self.model_reserved.display_unfolded_interactions(results)