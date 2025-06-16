from .typology import Typology
from itertools import permutations


class TypologyAmatoric(Typology):
    def __init__(self):
        super().__init__(["Love", "Passion", "Friendship", "Romance"])

    def get_aspects(self):
        return self.aspects

    def get_all_types(self):
        return [
            ", ".join([str(aspect) for aspect in perm])
            for perm in permutations(self.aspects, 4)
        ]

    def shorten_type(self, types):
        if isinstance(types, str):
            types = [types]
        return [
            "".join([aspect[0] for aspect in type_name.split(", ")])
            for type_name in types
        ]

    def determine_relationship_type(self, user1_type: str, user2_type: str) -> str:
        # Базовая логика: совпадение = Identity, иначе Unknown
        if user1_type == user2_type:
            return "Identity"
        return "Unknown Relationship"

    def get_comfort_score(self, relationship_type: str) -> (int, str):
        if relationship_type == "Identity":
            return 100, "Perfect alignment"
        return 0, "No known comfort score"


# Register in the global registry
from .registry import register_typology

register_typology("Amatoric", TypologyAmatoric)
