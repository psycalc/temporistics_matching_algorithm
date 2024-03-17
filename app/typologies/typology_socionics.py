import gettext
from itertools import product
from .typology import Typology
from flask_babel import lazy_gettext as _l

class TypologySocionics(Typology):
    def __init__(self, language="en"):
        self.set_language(language)
        super().__init__([
            _l("Intuitive Logical Extratim"),
            _l("Sensory Ethical Introtim"),
            _l("Ethical Sensory Extratim"),
            _l("Logical Intuitive Introtim"),
            _l("Intuitive Ethical Extratim"),
            _l("Sensory Logical Introtim"),
            _l("Logical Sensory Extratim"),
            _l("Ethical Intuitive Introtim")
        ])

    def set_language(self, language):
        global _
        try:
            lang_translation = gettext.translation('messages', localedir='locales', languages=[language])
            lang_translation.install()
            _ = lang_translation.gettext
        except Exception as e:
            # Fallback to default language or log error
            _ = gettext.gettext
            print(f"Error loading translation: {e}")  # Or use logging


    def get_all_types(self):
        valid_types = []
        aspects = ["Intuitive", "Sensory", "Ethical", "Logical"]
        traits = ["Extratim", "Introtim"]
        
        for aspect1 in aspects:
            for aspect2 in aspects:
                if aspect1 != aspect2:
                    for trait1 in traits:
                        for trait2 in traits:
                            if trait1 != trait2:
                                type_name = f"{aspect1} {aspect2} {trait1}"
                                valid_types.append(type_name)
        
        return valid_types

    def get_all_quadras(self):
        quadras = {
            'Alpha': {
                'types': [_l('Seeker (ILE)'), _l('Analyst (LII)'), _l('Enthusiast (ESE)'), _l('Mediator (SEI)')],
                'description': _l('The first quadra (Alpha) in socionics is defined by the aspects of Intuition of Possibilities, Structural Logic, Ethics of Emotions, and Sensation of Sensations. Its representatives value new opportunities and theories, inspiration, fun, and care for comfort. In the first quadra, stereotypical thinking is condemned - the ability to think creatively and fantasize is welcomed. Freedom of speech, striving for justice, and the search for truth are the main values of the representatives of this quadra.')
            },
            'Beta': {
                'types': [_l('Mentor (EIE)'), _l('Marshal (SLE)'), _l('Inspector (LSI)'), _l('Lyricist (IEI)')],
                'description': _l('The second quadra (Beta) in socionics is known as the Embodiers. The mission of the Embodiers quadra is to transform the initial concept into a complete ideology and implement new orders by creating corresponding organizational structures. The main characteristics of this rigid quadra are aristocracy (closedness, predominance of vertical, hierarchical, managerial ties) and resoluteness (decisiveness, great weight of volitional methods).')
            },
            'Gamma': {
                'types': [_l('Politician (SEE)'), _l('Entrepreneur (LIE)'), _l('Critic (ILI)'), _l('Guardian (ESI)')],
                'description': _l('The third quadra (Gamma) in socionics is known as the Reformers. The mission of the Reformers quadra is to remove the accumulated contradictions from the previous stage through criticism of admitted mistakes and carry out reform of rigid structures that have outlived their usefulness. The main characteristics of this quadra are democracy (openness, decentralization, diversity) and resoluteness (priority of power methods, decisive and active actions).')
            },
            'Delta': {
                'types': [_l('Administrator (LSE)'), _l('Master (SLI)'), _l('Advisor (IEE)'), _l('Humanist (EII)')],
                'description': _l('The fourth quadra (Delta) in socionics is known as the Perfectors. The mission of the Perfectors quadra is to bring the initial but reformed idea to exhaustion through improvement. The main characteristics of this quadra are aristocracy (closedness, elitism, quality of life) and discursiveness (deliberation, decision-making by non-violent methods).')
            }
        }
        return quadras

    def get_aspects(self):
        return self.aspects

    def shorten_type(self, typology_type):
        return typology_type

    @staticmethod
    def get_dual_type(type_name):
        duality_pairs = {
            'ILE': 'SEI',
            'SEI': 'ILE',
            'ESE': 'LII',
            'LII': 'ESE',
            'EIE': 'LSI',
            'LSI': 'EIE',
            'SLE': 'IEI',
            'IEI': 'SLE',
            'SEE': 'ILI',
            'ILI': 'SEE',
            'LIE': 'ESI',
            'ESI': 'LIE',
            'LSE': 'EII',
            'EII': 'LSE',
            'IEE': 'SLI',
            'SLI': 'IEE'
        }
        return duality_pairs.get(type_name)

    @staticmethod
    def get_activity_type(type_name):
        activity_pairs = {
            'ILE': 'ESE',
            'ESE': 'ILE',
            'SEI': 'LII',
            'LII': 'SEI',
            'EIE': 'SLE',
            'SLE': 'EIE',
            'LSI': 'IEI',
            'IEI': 'LSI',
            'SEE': 'LIE',
            'LIE': 'SEE',
            'ILI': 'ESI',
            'ESI': 'ILI',
            'LSE': 'IEE',
            'IEE': 'LSE',
            'EII': 'SLI',
            'SLI': 'EII'
        }
        return activity_pairs.get(type_name)