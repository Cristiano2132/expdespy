# src/expdespy/posthoc/posthoc_loader.py

from expdespy.posthoc import TukeyHSD, PairwiseTTest

POSTHOC_TESTS = {
    "tukey": TukeyHSD,
    "ttest": PairwiseTTest,
}


class PostHocLoader:
    """
    Loader: para criar instâncias de testes post hoc com base no nome.
    """

    @staticmethod
    def create(
        test_name: str,
        data,
        values_column: str,
        trats_column: str,
        alpha: float = 0.05,
    ):
        """
        Cria e retorna uma instância do teste post hoc correspondente.

        Args:
            test_name (str): Nome do teste ("tukey" or "ttest").
            data (pd.DataFrame): DataFrame com os dados.
            values_column (str): Nome da coluna com os valores/resposta.
            trats_column (str): Nome da coluna com os tratamentos/grupos.
            alpha (float): Nível de significância.

        Returns:
            Instância de uma subclasse de PostHocTest.
        """
        test_name = test_name.lower()
        if test_name not in POSTHOC_TESTS:
            raise ValueError(f"Teste post hoc '{test_name}' não é suportado.")

        test_class = POSTHOC_TESTS[test_name]
        return test_class(data=data, values_column=values_column, trats_column=trats_column, alpha=alpha)