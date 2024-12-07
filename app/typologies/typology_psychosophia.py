from .typology import Typology
from itertools import permutations


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

    def determine_relationship_type(self, user1_type: str, user2_type: str) -> str:
        """
        Здесь мы должны определить логику определения типа отношений.
        Пока можем упростить:
        - Если типы совпадают, возвращаем 'Identity'
        - Иначе 'Unknown Relationship'
        """
        if user1_type == user2_type:
            return "Identity"
        return "Unknown Relationship"

    def get_comfort_score(self, relationship_type: str) -> (int, str):
        """
        Возвращает комфорт-скор.
        Для примера:
        - Identity: 100
        - Unknown: 0
        """
        if relationship_type == "Identity":
            return 100, "Perfect alignment"
        return 0, "No known comfort score"
