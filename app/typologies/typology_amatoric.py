from .typology import Typology
from itertools import permutations


class TypologyAmatoric(Typology):
    def __init__(self):
        super().__init__(["Love", "Passion", "Friendship", "Romance"])

    # get aspects
    def get_aspects(self):
        return self.aspects

    def get_all_types(self):
        # Assuming temporistics involves combinations of its aspects just like the socionics example
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
