import unittest
from expdespy.datasets import load_fatorial_dic_nitrogenio_fosforo
from expdespy.models import FactorialCRD
from expdespy.datasets import fatorial_dic_irrigacao
import pandas as pd



class TestFactorialCRDExemploIrrigacao(unittest.TestCase):
    def test_load_fatorial_dic(self):
        df, description = fatorial_dic_irrigacao.load_fatorial_dic()

        # Verifica se retorna um DataFrame e um dicionário
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIsInstance(description, dict)

        # Verifica colunas esperadas
        expected_columns = ["f1", "f2", "produtividade"]
        self.assertTrue(all(col in df.columns for col in expected_columns))

        # Verifica se a resposta no description é coerente
        self.assertEqual(description["response"], "produtividade")

        # Verifica se fatores e níveis batem
        self.assertIn("f1", description["factors"])
        self.assertIn("f2", description["factors"])
        self.assertEqual(set(description["levels"]["f1"].keys()), {0, 1})
        self.assertEqual(set(description["levels"]["f2"].keys()), {0, 1})

        # Verifica tamanho e valores do DataFrame
        self.assertEqual(len(df), 12)
        self.assertTrue((df["f1"].isin([0, 1])).all())
        self.assertTrue((df["f2"].isin([0, 1])).all())

class TestFactorialCRD(unittest.TestCase):

    def setUp(self):
        # Arrange
        self.df, description = load_fatorial_dic_nitrogenio_fosforo()
        factors = description.get("factors")
        response = description.get("response")
        self.model = FactorialCRD(data=self.df, response=response, factors=factors)

    def test_anova_returns_dataframe(self):
        # Act
        result = self.model.anova()
        f_calc_axb = float(result.loc["C(f1):C(f2)", "F"])
        f_calc_axb_esperado = 4.95
        # Assert
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn("PR(>F)", result.columns)
        self.assertIn("F", result.columns)
        self.assertAlmostEqual(f_calc_axb, f_calc_axb_esperado, delta=0.1)

    def test_check_assumptions_returns_dict(self):
        # Act
        result = self.model.check_assumptions(print_conclusions=False)

        # Assert
        self.assertIsInstance(result, dict)
        self.assertIn("normality (Shapiro-Wilk)", result)
        self.assertIn("homoscedasticity (Levene)", result)

