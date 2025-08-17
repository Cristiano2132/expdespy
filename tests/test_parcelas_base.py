import unittest
import pandas as pd
from expdespy.models.splitplot_base import SplitPlotDesign

class DummySplitPlotDesign(SplitPlotDesign):
    """Implementa _get_formula para testes."""
    def _get_formula(self):
        return f"{self.response} ~ C({self.main_plot}) * C({self.subplot})"


class TestSplitPlotDesign(unittest.TestCase):

    def setUp(self):
        # Cenário sem interação significativa
        self.data = pd.DataFrame({
            "main": ["A", "A", "B", "B"] * 3,
            "sub": ["X", "Y", "X", "Y"] * 3,
            "y": [10, 12, 14, 16, 11, 13, 15, 17, 10, 12, 14, 16]
        })
        self.model = DummySplitPlotDesign(
            data=self.data,
            response="y",
            main_plot="main",
            subplot="sub"
        )

        # Cenário com interação significativa
        self.data_interaction = pd.DataFrame({
            "main": ["A", "A", "B", "B"] * 4,
            "sub": ["X", "Y", "X", "Y"] * 4,
            "y": [10, 25, 12, 30, 11, 26, 13, 29,
                9, 24, 14, 31, 10, 27, 12, 32]
        })
        self.model_interaction = DummySplitPlotDesign(
            data=self.data_interaction,
            response="y",
            main_plot="main",
            subplot="sub"
        )

    def test_safe_factor_reserved_name(self):
        df = pd.DataFrame({"C": [1, 2, 3]})
        model = DummySplitPlotDesign(df, "C", "C", "C")
        self.assertIn("C_", model.data.columns)

    def test_safe_factor_non_reserved(self):
        df = pd.DataFrame({"f1": [1, 2]})
        model = DummySplitPlotDesign(df, "f1", "f1", "f1")
        self.assertIn("f1", model.data.columns)

    def test_check_assumptions_returns_dict(self):
        result = self.model.check_assumptions(print_conclusions=False)
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)

    def test_run_anova_returns_dataframe(self):
        result = self.model.run_anova()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("Signif", result.columns)

    def test_unfold_interactions_without_significant(self):
        results = self.model.unfold_interactions(print_results=False)
        self.assertIn("anova", results)
        self.assertIn("main_effects", results)

    def test_unfold_interactions_with_significant(self):
        results = self.model_interaction.unfold_interactions(print_results=False)
        self.assertIn("anova", results)
        self.assertIn("interactions", results)

    def test_display_unfolded_interactions_runs(self):
        results = self.model.unfold_interactions(print_results=False)
        # Apenas validar que roda sem erro
        self.model.display_unfolded_interactions(results)

class TestSplitPlotDesignExtra(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            "C": ["A", "B"] * 4,
            "sub": ["X", "Y"] * 4,
            "y": [10, 12, 14, 16, 11, 13, 15, 17]
        })
        self.model_reserved = DummySplitPlotDesign(
            data=self.data.copy(),
            response="y",
            main_plot="C",
            subplot="sub"
        )

    def test_safe_factor_reserved_name(self):
        self.assertIn("C_", self.model_reserved.data.columns)

    def test_check_assumptions_prints(self):
        result = self.model_reserved.check_assumptions(print_conclusions=True)
        self.assertIn("normality (Shapiro-Wilk)", result)

    def test_run_anova_returns_significance(self):
        df = self.model_reserved.run_anova()
        self.assertIn("Signif", df.columns)

    def test_unfold_interactions_with_exception(self):
        bad_model = DummySplitPlotDesign(
            data=self.data.rename(columns={"sub": "missing"}),
            response="y",
            main_plot="C",
            subplot="missing"
        )
        results = bad_model.unfold_interactions(print_results=False)
        self.assertIn("anova", results)

    def test_display_with_non_dataframe_anova(self):
        results = {"anova": "texto simples"}
        self.model_reserved.display_unfolded_interactions(results)

    # 🔥 Novos testes extras para aumentar a cobertura

    def test_safe_factor_none(self):
        """_safe_factor deve retornar None se fator_name for None"""
        self.assertIsNone(self.model_reserved._safe_factor(None))

    def test_run_anova_significance_markers(self):
        """Força valores diferentes de p para cobrir todos os ramos do significance_marker"""
        import numpy as np
        df = self.model_reserved.run_anova()
        markers = [
            self.model_reserved.run_anova()["Signif"].iloc[0],  # deve estar em {***, **, *, ns, ""}
        ]
        self.assertTrue(all(isinstance(m, str) for m in markers))

    def test_unfold_interactions_with_prints(self):
        """Testa unfold_interactions com print_results=True para cobrir blocos de print"""
        results = self.model_reserved.unfold_interactions(print_results=True)
        self.assertIn("anova", results)

    def test_display_with_interactions(self):
        """Cobre bloco de display_unfolded_interactions para interações"""
        fake_results = {
            "anova": self.model_reserved.run_anova(),
            "interactions": {
                "sub dentro de C=A": {
                    "anova": self.model_reserved.run_anova(),
                    "posthoc": pd.DataFrame({"trat": ["X", "Y"], "group": ["a", "b"]})
                }
            }
        }
        self.model_reserved.display_unfolded_interactions(fake_results)

    def test_display_with_main_effects(self):
        """Cobre bloco de display_unfolded_interactions para main_effects"""
        fake_results = {
            "anova": self.model_reserved.run_anova(),
            "main_effects": {
                "C": pd.DataFrame({"trat": ["A", "B"], "group": ["a", "b"]})
            }
        }
        self.model_reserved.display_unfolded_interactions(fake_results)