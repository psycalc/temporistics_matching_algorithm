import gettext
from itertools import product
from .typology import Typology

_ = gettext.gettext

class TypologySocionics(Typology):
    def __init__(self, language="en"):
        """
        Initializes a new instance of the TypologySocionics class.
        """
        self.set_language(language)
        super().__init__([_("Ethics"), _("Logic"), _("Sensation"), _("Intuition"), _("Introversion"), _("Extraversion")])

    def set_language(self, language):
        """
        Set the language for translations.
        """
        global _  # Declare global at the beginning of the function
        try:
            lang_translation = gettext.translation('base', localedir='locales', languages=[language])
            lang_translation.install()
            _ = lang_translation.gettext
        except FileNotFoundError:
            _ = gettext.gettext  # Default to English if no translation

    def get_all_types(self):
        """
        Returns all valid combinations of aspects.
        
        A combination is valid if it does not contain both Ethics and Logic, Sensation and Intuition, or Introversion and Extraversion.
        """
        return ["".join([str(aspect[0]) for aspect in comb]) for comb in product(self.aspects, repeat=2)
                if not (("Ethics" in comb and "Logic" in comb) or
                        ("Sensation" in comb and "Intuition" in comb) or
                        ("Introversion" in comb and "Extraversion" in comb))]

    def get_all_quadras(self):
        """
        Returns all quadras of socionics with their descriptions.
        """
        quadras = {
            'Alpha': {
                'types': [_('Seeker (ILE)'), _('Analyst (LII)'), _('Enthusiast (ESE)'), _('Mediator (SEI)')],
                'description': _('The first quadra (Alpha) in socionics is defined by the aspects of Intuition of Possibilities, Structural Logic, Ethics of Emotions, and Sensation of Sensations. Its representatives value new opportunities and theories, inspiration, fun, and care for comfort. In the first quadra, stereotypical thinking is condemned - the ability to think creatively and fantasize is welcomed. Freedom of speech, striving for justice, and the search for truth are the main values of the representatives of this quadra.')
            },
            'Beta': {
                'types': [_('Mentor (EIE)'), _('Marshal (SLE)'), _('Inspector (LSI)'), _('Lyricist (IEI)')],
                'description': _('The second quadra (Beta) in socionics is known as the Embodiers. The mission of the Embodiers quadra is to transform the initial concept into a complete ideology and implement new orders by creating corresponding organizational structures. The main characteristics of this rigid quadra are aristocracy (closedness, predominance of vertical, hierarchical, managerial ties) and resoluteness (decisiveness, great weight of volitional methods).')
            },
            'Gamma': {
                'types': [_('Politician (SEE)'), _('Entrepreneur (LIE)'), _('Critic (ILI)'), _('Guardian (ESI)')],
                'description': _('The third quadra (Gamma) in socionics is known as the Reformers. The mission of the Reformers quadra is to remove the accumulated contradictions from the previous stage through criticism of admitted mistakes and carry out reform of rigid structures that have outlived their usefulness. The main characteristics of this quadra are democracy (openness, decentralization, diversity) and resoluteness (priority of power methods, decisive and active actions).')
            },
            'Delta': {
                'types': [_('Administrator (LSE)'), _('Master (SLI)'), _('Advisor (IEE)'), _('Humanist (EII)')],
                'description': _('The fourth quadra (Delta) in socionics is known as the Perfectors. The mission of the Perfectors quadra is to bring the initial but reformed idea to exhaustion through improvement. The main characteristics of this quadra are aristocracy (closedness, elitism, quality of life) and discursiveness (deliberation, decision-making by non-violent methods).')
            }
        }
        
        return quadras

    def get_aspects(self):
        """
        Returns the aspects of the socionics typology.
        """
        return self.aspects

    def shorten_type(self, typology_type):
        """
        Shortens the type if necessary.
        """
        return typology_type  # This can be modified to implement specific logic for shortening types

# Example usage
typology = TypologySocionics(language='ua')  # Assuming 'ua' is the code for Ukrainian
