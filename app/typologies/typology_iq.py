from .typology import Typology


class TypologyIQ(Typology):
    """Gentle IQ gradation: Aspiring, Balanced, and Insightful."""

    def __init__(self):
        super().__init__(["Aspiring", "Balanced", "Insightful"])

    def get_all_types(self):
        return self.aspects

    def shorten_type(self, types):
        if isinstance(types, str):
            types = [types]
        return [t[0] for t in types]

    def determine_relationship_type(self, user1_type: str, user2_type: str) -> str:
        if user1_type == user2_type:
            return "Identity"
        idx1 = self.aspects.index(user1_type)
        idx2 = self.aspects.index(user2_type)
        if abs(idx1 - idx2) == 1:
            return "Complementary"
        return "Contrast"

    def get_comfort_score(self, relationship_type: str) -> (int, str):
        if relationship_type == "Identity":
            return 80, "Similar cognitive style"
        if relationship_type == "Complementary":
            return 60, "Balanced perspectives"
        return 40, "Distinct approaches"


# Register in the global registry
from .registry import register_typology

register_typology("IQ", TypologyIQ)
