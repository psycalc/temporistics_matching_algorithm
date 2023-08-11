from itertools import permutations
from typology_aspect import TypologyAspect

class Typology:
    def __init__(self, aspects: list[str]):
        """
        Initializes a new instance of the Typology class.

        :param aspects: A list of aspect names.
        """
        self.aspects = [TypologyAspect(name, index) for index, name in enumerate(aspects, 1)]

    def get_all_types(self):
        """
        Prints all permutations of aspects.
        """
        # Get all permutations of aspects and print them
        for aspect_set in permutations(self.aspects):
            print(", ".join(map(str, aspect_set)))
