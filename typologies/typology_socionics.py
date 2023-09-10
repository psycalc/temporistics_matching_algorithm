from .typology import Typology
# import permutations from itertools
from itertools import permutations, combinations, product


class TypologySocionics(Typology):
    def __init__(self):
        """
        Initializes a new instance of the TypologySocionics class.
        """
        super().__init__(["Ethics", "Logic", "Sensation", "Intuition", "Introversion", "Extraversion"])


    def get_all_types(self):
        """
        Returns all valid combinations of aspects.
        
        A combination is valid if it does not contain both Ethics and Logic, Sensation and Intuition, or Introversion and Extraversion.
        """
        return ["".join([str(aspect[0]) for aspect in comb]) for comb in combinations(self.aspects, 3)
                if not (("Ethics" in comb and "Logic" in comb) or
                        ("Sensation" in comb and "Intuition" in comb) or
                        ("Introversion" in comb and "Extraversion" in comb))]

    
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
    
    # get aspects
    def get_aspects(self):
        return self.aspects
    
    def get_all_types(self):
        """
        Returns all 16 Socionics types.
        """
        dichotomies = [
            ['I', 'E'],
            ['S', 'N'],
            ['T', 'F'],
            ['J', 'P']
        ]
        return ["".join(combination) for combination in product(*dichotomies)]

    
    def shorten_type(self, typology_type):
        """
        Implement the logic for shortening the type if necessary.
        For now, it simply returns the original type, but you can
        add logic to shorten it in the future if needed.
        """
        return typology_type  # Placeholder. Modify based on actual requirements
