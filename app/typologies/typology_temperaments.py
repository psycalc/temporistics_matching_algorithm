from .typology import Typology

class TypologyTemperaments(Typology):
    """Classical four-temperament model."""

    def __init__(self):
        super().__init__(["Sanguine", "Choleric", "Melancholic", "Phlegmatic"])

    def get_all_types(self):
        return self.aspects

    def shorten_type(self, types):
        if isinstance(types, str):
            types = [types]
        return [t[0] for t in types]

    def determine_relationship_type(self, user1_type: str, user2_type: str) -> str:
        if user1_type == user2_type:
            return "Identity"
        pair = {user1_type, user2_type}
        if pair in [{"Sanguine", "Phlegmatic"}, {"Choleric", "Melancholic"}]:
            return "Complementary"
        return "Contrast"

    def get_comfort_score(self, relationship_type: str) -> (int, str):
        scores = {
            "Identity": (80, "Same temperament"),
            "Complementary": (70, "Balancing traits"),
            "Contrast": (50, "Different dispositions"),
        }
        return scores.get(relationship_type, (0, "Unknown Relationship"))
