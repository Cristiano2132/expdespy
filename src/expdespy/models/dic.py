from expdespy.models.base import ExperimentalDesign


class CRD(ExperimentalDesign):
    def _get_formula(self) -> str:
        return f"{self.response} ~ C({self.treatment})"
