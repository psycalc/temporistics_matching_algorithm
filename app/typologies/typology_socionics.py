import gettext
import json
import os
from .typology import Typology
from flask_babel import lazy_gettext as _l


class TypologySocionics(Typology):
    def __init__(self, language="en"):
        self.set_language(language)
        super().__init__(
            ["Intuitive", "Sensory", "Ethical", "Logical", "Extratim", "Introtim"]
        )

    def set_language(self, language):
        global _
        try:
            lang_translation = gettext.translation(
                "messages", localedir="locales", languages=[language]
            )
            lang_translation.install()
            _ = lang_translation.gettext
        except Exception as e:
            # Fallback to default language or log error
            _ = gettext.gettext
            print(f"Error loading translation: {e}")

    def get_all_types(self):
        return [
            _l("Seeker (ILE)"),
            _l("Analyst (LII)"),
            _l("Enthusiast (ESE)"),
            _l("Mediator (SEI)"),
            _l("Mentor (EIE)"),
            _l("Marshal (SLE)"),
            _l("Inspector (LSI)"),
            _l("Lyricist (IEI)"),
            _l("Politician (SEE)"),
            _l("Entrepreneur (LIE)"),
            _l("Critic (ILI)"),
            _l("Guardian (ESI)"),
            _l("Administrator (LSE)"),
            _l("Master (SLI)"),
            _l("Advisor (IEE)"),
            _l("Humanist (EII)"),
        ]

    def get_all_quadras(self):
        quadras = {
            "Alpha": {
                "types": [
                    _l("Seeker (ILE)"),
                    _l("Analyst (LII)"),
                    _l("Enthusiast (ESE)"),
                    _l("Mediator (SEI)"),
                ],
                "description": _l(
                    "The first quadra (Alpha) in socionics is defined by the aspects of Intuition of Possibilities, Structural Logic, Ethics of Emotions, and Sensation of Sensations. Its representatives value new opportunities and theories, inspiration, fun, and care for comfort."
                ),
            },
            "Beta": {
                "types": [
                    _l("Mentor (EIE)"),
                    _l("Marshal (SLE)"),
                    _l("Inspector (LSI)"),
                    _l("Lyricist (IEI)"),
                ],
                "description": _l(
                    "The second quadra (Beta) in socionics is known as the Embodiers. The mission of the Embodiers quadra is to transform the initial concept into a complete ideology and implement new orders by creating corresponding organizational structures."
                ),
            },
            "Gamma": {
                "types": [
                    _l("Politician (SEE)"),
                    _l("Entrepreneur (LIE)"),
                    _l("Critic (ILI)"),
                    _l("Guardian (ESI)"),
                ],
                "description": _l(
                    "The third quadra (Gamma) in socionics is known as the Reformers. The mission of the Reformers quadra is to remove the accumulated contradictions from the previous stage through criticism of admitted mistakes and carry out reform of rigid structures that have outlived their usefulness."
                ),
            },
            "Delta": {
                "types": [
                    _l("Administrator (LSE)"),
                    _l("Master (SLI)"),
                    _l("Advisor (IEE)"),
                    _l("Humanist (EII)"),
                ],
                "description": _l(
                    "The fourth quadra (Delta) in socionics is known as the Perfectors. The mission of the Perfectors quadra is to bring the initial but reformed idea to exhaustion through improvement."
                ),
            },
        }
        return quadras

    def get_aspects(self):
        return self.aspects

    def shorten_type(self, types):
        if isinstance(types, str):
            types = [types]
        return ["".join([word[0] for word in type_name.split()]) for type_name in types]

    @staticmethod
    def get_dual_type(type_name):
        duality_pairs = {
            "ILE": "SEI",
            "SEI": "ILE",
            "ESE": "LII",
            "LII": "ESE",
            "EIE": "LSI",
            "LSI": "EIE",
            "SLE": "IEI",
            "IEI": "SLE",
            "SEE": "ILI",
            "ILI": "SEE",
            "LIE": "ESI",
            "ESI": "LIE",
            "LSE": "EII",
            "EII": "LSE",
            "IEE": "SLI",
            "SLI": "IEE",
        }
        return duality_pairs.get(type_name)

    @staticmethod
    def get_activity_type(type_name):
        activity_pairs = {
            "ILE": "ESE",
            "ESE": "ILE",
            "SEI": "LII",
            "LII": "SEI",
            "EIE": "SLE",
            "SLE": "EIE",
            "LSI": "IEI",
            "IEI": "LSI",
            "SEE": "LIE",
            "LIE": "SEE",
            "ILI": "ESI",
            "ESI": "ILI",
            "LSE": "IEE",
            "IEE": "LSE",
            "EII": "SLI",
            "SLI": "EII",
        }
        return activity_pairs.get(type_name)

    def determine_relationship_type(self, user1_type: str, user2_type: str) -> str:
        """Return the intertype relation according to socionics theory."""

        if user1_type == user2_type:
            return "Identity"

        def code_from_name(name: str) -> str | None:
            """Extract 3‑letter socionics code from a full type name."""

            if not name:
                return None
            if "(" in name and name.endswith(")"):
                return name[name.rfind("(") + 1 : -1]
            return name if len(name) == 3 else None

        code1 = code_from_name(user1_type)
        code2 = code_from_name(user2_type)
        if not code1 or not code2:
            return "Unknown Relationship"

        to_4letter = {
            "ILE": "ENTP",
            "SEI": "ISFP",
            "ESE": "ESFJ",
            "LII": "INTJ",
            "EIE": "ENFJ",
            "LSI": "ISTJ",
            "SLE": "ESTP",
            "IEI": "INFP",
            "SEE": "ESFP",
            "ILI": "INTP",
            "LIE": "ENTJ",
            "ESI": "ISFJ",
            "LSE": "ESTJ",
            "EII": "INFJ",
            "IEE": "ENFP",
            "SLI": "ISTP",
        }

        try:
            mbti1 = to_4letter[code1]
            mbti2 = to_4letter[code2]
        except KeyError:
            return "Unknown Relationship"

        from socionics.core import Stype, Sociodb

        db = Sociodb()
        try:
            relation_index = Stype(mbti1).otn(Stype(mbti2))
            russian = db.otn[relation_index]
        except Exception:
            return "Unknown Relationship"

        relation_map = {
            "Тождественные": "Identity",
            "Квазитождество": "Quasi-identity",
            "Родственные": "Kindred",
            "Исполнитель": "Business",
            "Деловые": "Business",
            "Заказчик": "Request",
            "Суперэго": "Super-ego",
            "Активация": "Activation",
            "Противоположность": "Conflict",
            "Зеркальные": "Mirror",
            "Миражные": "Illusionary",
            "Ревизор": "Supervision",
            "Полудуальные": "Semi-duality",
            "Подревизный": "Supervisor",
            "Дуальные": "Duality",
            "Конфликтные": "Conflict",
        }

        return relation_map.get(russian, "Unknown Relationship")

    def get_comfort_score(self, relationship_type: str) -> (int, str):
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        )
        path = os.path.join(base_dir, "data", "socionics_relationships.json")
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except Exception:
            data = {}
        info = data.get(
            relationship_type, {"score": 0, "description": "Unknown Relationship"}
        )
        return info.get("score", 0), info.get("description", "")


# Register in the global registry
from .registry import register_typology

register_typology("Socionics", TypologySocionics)
