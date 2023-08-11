from typology import Typology
# import permutations from itertools
from itertools import permutations
class TypologySocionics(Typology):
    def __init__(self):
        """
        Initializes a new instance of the TypologySocionics class.
        """
        super().__init__(["Ethics", "Logic", "Sensation", "Intuition", "Introversion", "Extraversion"])

    def get_all_types(self):
        """
        Prints all valid permutations of aspects.
        
        A permutation is valid if it does not contain both Ethics and Logic, Sensation and Intuition, or Introversion and Extraversion.
        """
        types = [", ".join([str(aspect) for aspect in perm]) for perm in permutations(self.aspects, 4)
                 if not (("Ethics" in perm and "Logic" in perm) or
                         ("Sensation" in perm and "Intuition" in perm) or
                         ("Introversion" in perm and "Extraversion" in perm))]
        
        print("\n".join(types))