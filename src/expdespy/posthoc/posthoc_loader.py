# src/expdespy/posthoc/posthoc_loader.py


from expdespy.posthoc import TukeyHSD, PairwiseTTest

POSTHOC_TESTS = {
    "tukey": TukeyHSD,
    "ttest": PairwiseTTest,
}


class PostHocLoader:
    """
    Loader class to create instances of post hoc tests based on the given name.
    """

    @staticmethod
    def create(
        test_name: str,
        data,
        values_column: str,
        treatments_column: str,
        alpha: float = 0.05,
    ):
        """
        Create and return an instance of the corresponding post hoc test.

        Args:
            test_name (str): Name of the test ("tukey" or "ttest").
            data (pd.DataFrame): DataFrame containing the experimental data.
            values_column (str): Name of the column with response values.
            treatments_column (str): Name of the column with treatments/groups.
            alpha (float): Significance level. Default is 0.05.

        Returns:
            PostHocTest: An instance of a PostHocTest subclass.
        """
        test_name = test_name.lower()
        if test_name not in POSTHOC_TESTS:
            raise ValueError(f"Post hoc test '{test_name}' is not supported.")

        test_class = POSTHOC_TESTS[test_name]
        return test_class(
            data=data,
            values_column=values_column,
            treatments_column=treatments_column,
            alpha=alpha
        )
