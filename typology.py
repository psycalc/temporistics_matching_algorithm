from itertools import permutations
from typology_aspect import TypologyAspect

class Typology:
    def __init__(self, aspects: list[str], quadras: list[list[str]]):
        self.aspects = [TypologyAspect(name, index) for index, name in enumerate(aspects, 1)]
        self.quadras = quadras

    def get_all_types(self) -> list[str]:
        return [", ".join(map(str, aspect_set)) for aspect_set in permutations(self.aspects)]

    def print_all_types(self):
        for aspect_set in self.get_all_types():
            print(aspect_set)

    def print_quadras(self):
        for index, quadra in enumerate(self.quadras, 1):
            print(f"Quadra {index}: {', '.join(quadra)}")
    
    def get_all_quadras(self):
        """
        Returns all valid quadras of the typology.
        
        A quadra is valid if it contains one aspect from each dichotomy.
        """
        raise NotImplementedError("This method must be implemented by a subclass.")
