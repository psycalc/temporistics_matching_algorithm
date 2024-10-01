from typing import List
from itertools import permutations
from typology import Typology  # Импортируем ваш базовый абстрактный класс

class TypologyTemporistics(Typology):  # Наследуем от Typology
    def __init__(self):
        """
        Initializes a new instance of the TypologyTemporistics class.
        Temporistics is based on four key time aspects: Past, Present, Future, and Eternity.
        """
        super().__init__(["Past", "Present", "Future", "Eternity"])  # Инициализация базового класса

    TETRADS = {
        '6-1-2': "Era of Individuality (P)",
        '2-3-4': "Era of Order (E)",
        '4-5-6': "Era of Movement (F)",
        '1-5-3': "Golden Age of Every Era (N)"
    }

    QUADRAS_AND_DESCRIPTIONS = {
        'Antipodes': {
            'types': ["Game Master", "Maestro", "Player", "Politician"],
            'description': 'Antipodes are one-plane N and P. Fixed position in all senses, focused on self-image and manipulation.'
        },
        'Guardians and Border Guards': {
            'types': ["Missionary", "Standard Bearer", "Rescuer", "Knight"],
            'description': 'Guardians and Border Guards are one-plane V and P. Focused on self-image and the search for place, with manipulation.'
        },
        'Old-timers and Founders': {
            'types': ["Theorist", "Oracle", "Conqueror", "Star"],
            'description': 'Old-timers and founders are one-plane N and V. Fixed place and existence with manipulation.'
        },
        'Conductors': {
            'types': ["Ideologist", "Samurai", "Colonist", "Pioneer"],
            'description': 'Conductors are one-plane B and V. Fixed direction and existence, with manipulation.'
        },
        'Scouts and Scouts': {
            'types': ["Scout", "Hacker", "Gray Cardinal", "Taster"],
            'description': 'Scouts are one-plane N and B. Fixed place and development with manipulation.'
        },
        'Nomads and Tramps': {
            'types': ["Tamada", "Pathfinder", "Robinson", "Initiator"],
            'description': 'Nomads and Tramps are one-plane P and B. Self-image and development are fixed; existence is manipulated.'
        }
    }

    QUADRAS = {
        quadra_name: data['types'] for quadra_name, data in QUADRAS_AND_DESCRIPTIONS.items()
    }

    QUADRA_DESCRIPTIONS = {
        quadra_name: data['description'] for quadra_name, data in QUADRAS_AND_DESCRIPTIONS.items()
    }

    def validate_tetrad_sequence(self, tetrad_sequence: str) -> None:
        """
        Validates a tetrad sequence.
        """
        if tetrad_sequence not in self.TETRADS:
            raise ValueError(f"Invalid tetrad sequence: {tetrad_sequence}")

    def get_tetrads(self, tetrad_sequence: str) -> str:
        """
        Returns the description for a given tetrad sequence.
        """
        self.validate_tetrad_sequence(tetrad_sequence)
        return self.TETRADS.get(tetrad_sequence, "Unknown Tetrad")

    def get_quadras(self, quadra_name: str) -> List[str]:
        """
        Returns the list of types for a given quadra.
        """
        if quadra_name not in self.QUADRAS:
            raise ValueError(f"Invalid quadra name: {quadra_name}")
        return self.QUADRAS[quadra_name]

    def get_quadra_description(self, quadra_name: str) -> str:
        """
        Returns the description for a given quadra.
        """
        if quadra_name not in self.QUADRA_DESCRIPTIONS:
            raise ValueError(f"Invalid quadra name: {quadra_name}")
        return self.QUADRA_DESCRIPTIONS[quadra_name]

    @staticmethod
    def get_time_periods_short(time_periods: List[str]) -> List[str]:
        """
        Returns the shortened form of the time periods.
        """
        time_periods_short = []
        for period in time_periods:
            if period == "Present":
                period = "Current"
            time_periods_short.append(period[0])
        return time_periods_short

    INTER_TYPE_RELATIONSHIPS = {
        ("Past", "Present"): "Superficial Agreement",
        ("Future", "Eternity"): "Shared Vision",
        ("Past", "Past"): "Complete Unity",
        ("Present", "Future"): "Strategic Conflict",
    }

    def get_intertype_relationship(self, type1: str, type2: str) -> str:
        """
        Returns the intertype relationship between two given types.
        """
        relationship = self.INTER_TYPE_RELATIONSHIPS.get((type1, type2), None)
        if relationship is None:
            raise ValueError(f"Intertype relationship between {type1} and {type2} is not defined.")
        return relationship

    def get_comfort_score(self, relationship_type: str):
        """
        Returns a comfort score based on the relationship type.
        """
        comfort_scores = {
            "Complete Unity": (100, "Perfect alignment in all priorities."),
            "Deep Harmony": (90, "Top two time priorities match, leading to significant harmony."),
            "Shared Vision": (75, "Top three priorities align, resulting in cooperation."),
            "Superficial Agreement": (50, "Only the last priority matches, shallow agreement."),
            "Strategic Conflict": (40, "Differences lead to friction, but can stimulate growth."),
            "Surface Influence": (30, "Minor overlap in low priorities."),
            "Temporal Tension": (25, "Constant tension due to opposing priorities."),
            "Illusion of Compatibility": (20, "Appears aligned on the surface, but mismatched in critical areas."),
        }
        return comfort_scores.get(relationship_type, (0, "Unknown relationship type"))

    def determine_relationship_type(self, user1_type: str, user2_type: str):
        """
        Determines the relationship type between two users based on their time perspectives.
        """
        user1_priority = user1_type.split(", ")[0]  # Highest priority time aspect
        user2_priority = user2_type.split(", ")[0]

        return self.get_intertype_relationship(user1_priority, user2_priority)

    def get_all_types(self):
        """
        Returns all possible combinations of time perspectives (aspects).
        """
        return [", ".join([str(aspect) for aspect in perm]) for perm in permutations(self.aspects, 4)]

    def shorten_type(self, types: List[str]) -> List[str]:
        """
        Shortens the representation of types by converting the aspects into their initials.
        """
        if isinstance(types, str):
            types = [types]
        return ["".join([aspect[0] for aspect in type_name.split(", ")]) for type_name in types]
