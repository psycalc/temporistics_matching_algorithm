from .typology import Typology
from itertools import permutations

class TypologyPsychosophia(Typology):
    def __init__(self):
        """
        Initializes a new instance of the TypologyPsychosophia class.
        """
        super().__init__(["Emotion", "Logic", "Will", "Power"])
    
    def get_all_quadras(self):
        """
        Returns all quadras of psychosophy with their descriptions.
        
        Each quadra consists of four types that share common values and characteristics.
        """
        quadras = {
            'First': {
                'types': ['Andersen (ELWF)', 'Ghazali (EWLV)', 'Goethe (PWLE)', 'Aristippus (PLWE)'],
                'description': 'The first psychosophic quadra is characterized by processional Will and Logic, as well as resultative Physics and Emotion. Its representatives value arguments and heated discussions.'
            },
            'Second': {
                'types': ['Pushkin (EPWL)', 'Pasternak (EWPL)', 'Lao Tzu (LPWE)', 'Plato (LWPE)'],
                'description': 'The second psychosophic quadra is characterized by processional Will and Physics, as well as resultative Emotion and Logic. It is known for silent thinking and team collaboration.'
            },
            'Third': {
                'types': ['Rousseau (ELFW)', 'Bukharin (EWFL)', 'Napoleon (PFLW)', 'Lenin (PLWF)'],
                'description': 'The third psychosophic quadra is characterized by processional Physics and Logic, as well as resultative Will and Emotion. Its representatives are known for intellectual pursuits and appreciation of aesthetics.'
            }
        }
        return quadras
    
    def get_aspects(self):
        """
        Returns the list of aspects for Psychosophia.
        """
        return self.aspects
    
    def get_all_types(self):
        """
        Returns all possible combinations of psychosophic aspects.
        
        :return: A list of all possible combinations (permutations) of the aspects.
        """
        return [", ".join([str(aspect) for aspect in perm]) for perm in permutations(self.aspects, 4)]

    def shorten_type(self, types):
        """
        Shortens the representation of types by converting the aspects into their initials.

        :param types: A list or string representing types (e.g., "Emotion, Logic, Will, Power").
        :return: A list of shortened type strings (e.g., "E,L,W,P").
        """
        if isinstance(types, str):
            types = [types]
        return ["".join([aspect[0] for aspect in type_name.split(", ")]) for type_name in types]
