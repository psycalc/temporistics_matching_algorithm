from .typology import Typology
from itertools import permutations
from typing import List


class TypologyPsychosophia(Typology):
    """
    TypologyPsychosophia class represents the typology based on Psychosophy,
    which includes four aspects: Emotion, Logic, Will, and Physics.
    """

    def __init__(self):
        """
        Initializes a new instance of the TypologyPsychosophia class.
        """
        # Aspects in Psychosophy: Emotion (E), Logic (L), Will (W), Physics (F)
        super().__init__(["Emotion", "Logic", "Will", "Physics"])

    def get_all_quadras(self):
        quadras = {
            "First Quadra": {
                "types": [
                    "Gandhi (EFLW)",
                    "Van Gogh (EFLW)",
                    "Mother Teresa (EFLW)",
                    "Mozart (EFLW)",
                    "Andersen (EFLW)",
                    "Ghazali (EFLW)",
                ],
                "description": "Characterized by a strong emphasis on Emotion and Physics. Values harmony, creativity, and aesthetic expression.",
            },
            "Second Quadra": {
                "types": [
                    "Napoleon (FEWL)",
                    "Lenin (FEWL)",
                    "Hitler (FEWL)",
                    "Joan of Arc (FEWL)",
                    "Alexander the Great (FEWL)",
                    "Catherine the Great (FEWL)",
                ],
                "description": "Emphasizes Physics and Emotion with a focus on action and transformation. Values determination and influence.",
            },
            "Third Quadra": {
                "types": [
                    "Einstein (LEFW)",
                    "Descartes (LEFW)",
                    "Newton (LEFW)",
                    "Spinoza (LEFW)",
                    "Kant (LEFW)",
                    "Hegel (LEFW)",
                ],
                "description": "Centers on Logic and Emotion. Values knowledge, exploration, and understanding.",
            },
            "Fourth Quadra": {
                "types": [
                    "Steve Jobs (LWEF)",
                    "Bill Gates (LWEF)",
                    "Mark Zuckerberg (LWEF)",
                    "Elon Musk (LWEF)",
                    "Nikola Tesla (LWEF)",
                    "Warren Buffett (LWEF)",
                ],
                "description": "Focuses on Logic and Will. Values innovation, leadership, and strategic thinking.",
            },
            "Fifth Quadra": {
                "types": [
                    "Buddha (WELF)",
                    "Lao Tzu (WELF)",
                    "Dalai Lama (WELF)",
                    "Confucius (WELF)",
                    "Socrates (WELF)",
                    "Plato (WELF)",
                ],
                "description": "Emphasizes Will and Emotion. Values wisdom, introspection, and philosophical contemplation.",
            },
            "Sixth Quadra": {
                "types": [
                    "Machiavelli (WFEL)",
                    "Stalin (WFEL)",
                    "Vladimir Putin (WFEL)",
                    "Donald Trump (WFEL)",
                    "Julius Caesar (WFEL)",
                    "Genghis Khan (WFEL)",
                ],
                "description": "Centers on Will and Physics. Values power, control, and pragmatic action.",
            },
        }
        return quadras

    def get_aspects(self):
        return self.aspects

    def get_all_types(self):
        return [", ".join(perm) for perm in permutations(self.aspects, 4)]

    def shorten_type(self, types):
        if isinstance(types, str):
            types = [types]
        elif not isinstance(types, list):
            raise TypeError("Input must be a string or a list of strings.")
        shortened_types = []
        for type_name in types:
            if not isinstance(type_name, str):
                raise TypeError("All items in the list must be strings.")
            initials = "".join([aspect[0] for aspect in type_name.split(", ")])
            shortened_types.append(initials)
        return shortened_types

    def _parse_type_to_list(self, type_str):
        """Parse a type string into a list of aspects."""
        if not type_str:
            return []
        return type_str.split(", ")

    def are_types_identity_philia(self, type1: List[str], type2: List[str]) -> bool:
        """Check if the types are identical or share the first two aspects."""
        return type1 == type2 or type1[:2] == type2[:2]

    def are_types_extinguishment(self, type1: List[str], type2: List[str]) -> bool:
        """Check if the types form an Extinguishment relationship."""
        # Extinguishment occurs when the aspect order is completely reversed
        return type1 == list(reversed(type2))

    def are_types_full_eros(self, type1: List[str], type2: List[str]) -> bool:
        """Return True when the types have a Full Eros relationship."""
        # Happens when the first two aspects of one type are the other's
        # third and fourth aspects, and vice versa. Excludes Extinguishment
        # and Identity cases.
        if self.are_types_extinguishment(type1, type2) or type1 == type2:
            return False

        # Condition 1: first two of type1 match last two of type2
        cond1 = set(type1[:2]) == set(type2[2:])
        # Condition 2: last two of type1 match first two of type2
        cond2 = set(type1[2:]) == set(type2[:2])
        # Both conditions must hold for Eros
        return cond1 and cond2

    def are_types_full_agape(self, type1: List[str], type2: List[str]) -> bool:
        """Check for a Full Agape relationship between types."""
        # New rule: a complete mirror match (1<->4 and 2<->3) counts as
        # Full Agape. This needs to be evaluated before Extinguishment.
        if type1 == list(reversed(type2)):
            return True

        # Occurs when the first two aspects of one type are the other's third
        # and fourth, but not vice versa. Not Extinguishment, Eros or Identity.
        if self.are_types_extinguishment(type1, type2) or type1 == type2:
            return False

        # Condition 1: first two of type1 match last two of type2
        cond1 = set(type1[:2]) == set(type2[2:])
        # Condition 2: last two of type1 match first two of type2
        cond2 = set(type1[2:]) == set(type2[:2])

        # Special case: both conditions true means Eros
        is_eros = cond1 and cond2

        # Agape requires exactly one of the conditions to hold (XOR) and it must
        # not be the Eros case already checked in determine_relationship_type.
        return (cond1 or cond2) and not is_eros

    def are_types_order_full_order(self, type1: List[str], type2: List[str]) -> bool:
        """Check if the types form an Order or Full Order relationship."""
        # Occurs when the first aspect of one type is the second of the other and vice versa
        return type1[0] == type2[1] and type1[1] == type2[0]

    def are_types_mirage(self, type1: List[str], type2: List[str]) -> bool:
        """Return True if the types form a Mirage relationship."""
        # First aspect of one type is the third of the other and vice versa
        return type1[0] == type2[2] and type1[2] == type2[0]

    def are_types_revision(self, type1: List[str], type2: List[str]) -> bool:
        """Check for a Revision relationship between two types."""
        # First aspect of one type is the fourth of the other and vice versa
        return type1[0] == type2[3] and type1[3] == type2[0]

    def are_types_therapy_attraction(self, type1: List[str], type2: List[str]) -> bool:
        """Return True for a Therapy-Attraction relationship."""
        # Second aspect of one type is the third of the other and vice versa
        return type1[1] == type2[2] and type1[2] == type2[1]

    def are_types_therapy_misunderstanding(
        self, type1: List[str], type2: List[str]
    ) -> bool:
        """Check for a Therapy-Misunderstanding relationship."""
        # Second aspect of one type is the other's fourth, but not vice versa
        cond1 = type1[1] == type2[3] and type1[3] != type2[1]
        cond2 = type2[1] == type1[3] and type2[3] != type1[1]
        return (
            cond1 or cond2
        )  # Implicit XOR, as both true would imply Extinguishment in some cases (e.g. 1234 vs 4321)

    def are_types_conflict_submission_dominance(
        self, type1: List[str], type2: List[str]
    ) -> bool:
        """Return True when one type dominates and the other submits."""
        # Occurs when the leading aspect of one type is a weakness (3rd or 4th position) of the other
        # Special case removed
        cond1 = type1[0] in type2[2:] and type2[0] not in type1[2:]
        cond2 = type2[0] in type1[2:] and type1[0] not in type2[2:]
        return cond1 or cond2  # Implicit XOR logic

    def determine_relationship_type(self, user1_type: str, user2_type: str) -> str:
        """Determine the relationship between two Psychosophy types.

        Checks are performed in a strict order to avoid ambiguous results.
        """
        user1_aspects = self._parse_type_to_list(user1_type)
        user2_aspects = self._parse_type_to_list(user2_type)

        if (
            not user1_aspects
            or not user2_aspects
            or len(user1_aspects) != 4
            or len(user2_aspects) != 4
        ):
            return "Unknown Relationship"  # Basic validation

        # Aspect validity check can be added here if needed
        # all_aspects_valid = all(aspect in self.aspects for aspect in user1_aspects + user2_aspects)
        # if not all_aspects_valid:
        #     return "Unknown Relationship"

        # 1. Identity/Philia
        if self.are_types_identity_philia(user1_aspects, user2_aspects):
            return "Identity/Philia"

        # 2. Full Agape (including mirror cases)
        if self.are_types_full_agape(user1_aspects, user2_aspects):
            return "Full Agape"

        # 3. Extinguishment
        if self.are_types_extinguishment(user1_aspects, user2_aspects):
            return "Psychosophia Extinguishment"

        # 4. Full Eros
        if self.are_types_full_eros(user1_aspects, user2_aspects):
            return "Full Eros"

        # 5. Order/Full Order
        if self.are_types_order_full_order(user1_aspects, user2_aspects):
            return "Order/Full Order"

        # 6. Mirage
        if self.are_types_mirage(user1_aspects, user2_aspects):
            return "Mirage"

        # 7. Revision
        if self.are_types_revision(user1_aspects, user2_aspects):
            return "Revision"

        # 8. Therapy-Attraction
        if self.are_types_therapy_attraction(user1_aspects, user2_aspects):
            return "Therapy-Attraction"

        # 9. Therapy-Misunderstanding
        if self.are_types_therapy_misunderstanding(user1_aspects, user2_aspects):
            return "Therapy-Misunderstanding"

        # 10. Conflict Submission/Dominance
        if self.are_types_conflict_submission_dominance(user1_aspects, user2_aspects):
            return "Conflict Submission/Dominance"

        # 11. Neutrality (when none of the above matched)
        return "Neutrality"

    def get_comfort_score(self, relationship_type: str) -> (int, str):
        """Return the comfort score and description for a relationship type."""
        # relationship_type: name of the relationship in English
        comfort_scores = {
            "Identity/Philia": (9, "Взаємодія легка, комфортна і дружня"),
            "Full Eros": (
                8,
                "Взаємодія динамічна, стимулююча і сповнена взаємного інтересу",
            ),
            "Full Agape": (10, "Взаємодія комфортна, гармонійна і взаємовигідна"),
            "Psychosophia Extinguishment": (
                -5,
                "Взаємодія віддалена, формальна з взаємоповагою",
            ),
            "Neutrality": (
                0,
                "Взаємодія нейтральна і ввічлива, але без глибокого розуміння",
            ),
            "Mirage": (3, "Взаємодія непередбачувана, інтенсивна і емоційно заряджена"),
            "Order/Full Order": (
                6,
                "Взаємодія асиметрична, один партнер більш активний і домінуючий",
            ),
            "Revision": (
                -3,
                "Взаємодія складна і конфронтаційна, але може вести до росту",
            ),
            "Therapy-Misunderstanding": (
                2,
                "Взаємодія комфортна і легка через спільні цінності",
            ),
            "Therapy-Attraction": (
                4,
                "Взаємодія асиметрична, один партнер більш активний і підтримуючий",
            ),
            "Conflict Submission/Dominance": (
                -4,
                "Взаємодія характеризується боротьбою за владу і конфліктами",
            ),
        }

        return comfort_scores.get(relationship_type, (0, "Невідомий тип відносин"))


# Register in the global registry
from .registry import register_typology

register_typology("Psychosophia", TypologyPsychosophia)
