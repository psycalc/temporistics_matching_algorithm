from typology import Typology
# import permutations from itertools
from itertools import permutations

class TypologySocionics(Typology):
    def __init__(self):
        """
        Initializes a new instance of the TypologySocionics class.
        """
        super().__init__(["Ethics", "Logic", "Sensation", "Intuition", "Introversion", "Extraversion"], [])

    def get_all_types(self):
        """
        Returns all valid permutations of aspects.
        
        A permutation is valid if it does not contain both Ethics and Logic, Sensation and Intuition, or Introversion and Extraversion.
        """
        return [", ".join([str(aspect) for aspect in perm]) for perm in permutations(self.aspects, 4)
                 if not (("Ethics" in perm and "Logic" in perm) or
                         ("Sensation" in perm and "Intuition" in perm) or
                         ("Introversion" in perm and "Extraversion" in perm))]
    
    def get_all_quadras(self):
        """
        Returns all quadras of socionics with their descriptions.
        
        Each quadra consists of four types that share common values and characteristics.
        """
        quadras = {
            'Alpha': {
                'types': ['Seeker (ILE)', 'Analyst (LII)', 'Enthusiast (ESE)', 'Mediator (SEI)'],
                'description': 'The first quadra (Alpha) in socionics is defined by the aspects of Intuition of Possibilities, Structural Logic, Ethics of Emotions, and Sensation of Sensations. Its representatives value new opportunities and theories, inspiration, fun, and care for comfort. In the first quadra, stereotypical thinking is condemned - the ability to think creatively and fantasize is welcomed. Freedom of speech, striving for justice, and the search for truth are the main values of the representatives of this quadra.'
            },
            'Beta': {
                'types': ['Mentor (EIE)', 'Marshal (SLE)', 'Inspector (LSI)', 'Lyricist (IEI)'],
                'description': 'The second quadra (Beta) in socionics is known as the Embodiers. The mission of the Embodiers quadra is to transform the initial concept into a complete ideology and implement new orders by creating corresponding organizational structures. The main characteristics of this rigid quadra are aristocracy (closedness, predominance of vertical, hierarchical, managerial ties) and resoluteness (decisiveness, great weight of volitional methods).'
            },
            'Gamma': {
                'types': ['Politician (SEE)', 'Entrepreneur (LIE)', 'Critic (ILI)', 'Guardian (ESI)'],
                'description': 'The third quadra (Gamma) in socionics is known as the Reformers. The mission of the Reformers quadra is to remove the accumulated contradictions from the previous stage through criticism of admitted mistakes and carry out reform of rigid structures that have outlived their usefulness. The main characteristics of this quadra are democracy (openness, decentralization, diversity) and resoluteness (priority of power methods, decisive and active actions).'
            },
            'Delta': {
                'types': ['Administrator (LSE)', 'Master (SLI)', 'Advisor (IEE)', 'Humanist (EII)'],
                'description': 'The fourth quadra (Delta) in socionics is known as the Perfectors. The mission of the Perfectors quadra is to bring the initial but reformed idea to exhaustion through improvement. The main characteristics of this quadra are aristocracy (closedness, elitism, quality of life) and discursiveness (deliberation, decision-making by non-violent methods).'
            }
        }
        
        return quadras
