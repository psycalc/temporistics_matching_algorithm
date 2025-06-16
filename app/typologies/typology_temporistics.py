from typing import List, Tuple, Dict
from itertools import permutations, product


# Assuming Typology is an abstract base class that we're inheriting from.
class Typology:
    def __init__(self, aspects: List[str]):
        self.aspects = aspects


class TypologyTemporistics(Typology):
    """
    TypologyTemporistics class represents a typology based on four temporal aspects:
    Past, Current, Future, and Eternity. It provides methods to work with tetrads,
    quadras, and intertype relationships based on these temporal perspectives.
    """

    def __init__(self):
        """
        Initializes a new instance of the TypologyTemporistics class with four temporal aspects.
        """
        # Renamed 'Present' to 'Current' to avoid confusion when shortened (both Past and Present start with 'P').
        super().__init__(["Past", "Current", "Future", "Eternity"])

    # Dictionary mapping tetrad sequences to their descriptions.
    TETRADS: Dict[str, str] = {
        "6-1-2": "Era of Individuality (P)",
        "2-3-4": "Era of Order (E)",
        "4-5-6": "Era of Movement (F)",
        "1-5-3": "Golden Age of Each Era (C)",
    }

    # Dictionary containing quadras with their types and descriptions.
    QUADRAS_AND_DESCRIPTIONS: Dict[str, Dict[str, List[str]]] = {
        "Antipodes": {
            "types": ["Game Master", "Maestro", "Player", "Politician"],
            "description": "Antipodes are one-plane C and P. Fixed position in all senses, focused on self-image and manipulation.",
        },
        "Guardians and Border Guards": {
            "types": ["Missionary", "Standard Bearer", "Rescuer", "Knight"],
            "description": "Guardians and Border Guards are one-plane F and P. Focused on self-image and the search for place, with manipulation.",
        },
        "Old-timers and Founders": {
            "types": ["Theorist", "Oracle", "Conqueror", "Star"],
            "description": "Old-timers and Founders are one-plane C and F. Fixed place and existence with manipulation.",
        },
        "Conductors": {
            "types": ["Ideologist", "Samurai", "Colonist", "Pioneer"],
            "description": "Conductors are one-plane E and F. Fixed direction and existence, with manipulation.",
        },
        "Scouts": {
            "types": ["Scout", "Hacker", "Gray Cardinal", "Taster"],
            "description": "Scouts are one-plane C and E. Fixed place and development with manipulation.",
        },
        "Nomads and Tramps": {
            "types": ["Tamada", "Pathfinder", "Robinson", "Initiator"],
            "description": "Nomads and Tramps are one-plane P and E. Self-image and development are fixed; existence is manipulated.",
        },
    }

    # Separate dictionaries for quadras and their descriptions.
    QUADRAS: Dict[str, List[str]] = {
        quadra_name: data["types"]
        for quadra_name, data in QUADRAS_AND_DESCRIPTIONS.items()
    }

    QUADRA_DESCRIPTIONS: Dict[str, str] = {
        quadra_name: data["description"]
        for quadra_name, data in QUADRAS_AND_DESCRIPTIONS.items()
    }

    def validate_tetrad_sequence(self, tetrad_sequence: str) -> None:
        """
        Validates if the given tetrad sequence is valid.

        Args:
            tetrad_sequence (str): The tetrad sequence to validate.

        Raises:
            ValueError: If the tetrad sequence is invalid.
        """
        if tetrad_sequence not in self.TETRADS:
            raise ValueError(f"Invalid tetrad sequence: {tetrad_sequence}")

    def get_tetrad_description(self, tetrad_sequence: str) -> str:
        """
        Retrieves the description for a given tetrad sequence.

        Args:
            tetrad_sequence (str): The tetrad sequence identifier.

        Returns:
            str: The description of the tetrad.

        Raises:
            ValueError: If the tetrad sequence is invalid.
        """
        self.validate_tetrad_sequence(tetrad_sequence)
        return self.TETRADS[tetrad_sequence]

    def get_quadra_types(self, quadra_name: str) -> List[str]:
        """
        Retrieves the list of types for a specified quadra.

        Args:
            quadra_name (str): The name of the quadra.

        Returns:
            List[str]: A list of type names associated with the quadra.

        Raises:
            ValueError: If the quadra name is invalid.
        """
        if quadra_name not in self.QUADRAS:
            raise ValueError(f"Invalid quadra name: {quadra_name}")
        return self.QUADRAS[quadra_name]

    def get_quadra_description(self, quadra_name: str) -> str:
        """
        Retrieves the description for a specified quadra.

        Args:
            quadra_name (str): The name of the quadra.

        Returns:
            str: The description of the quadra.

        Raises:
            ValueError: If the quadra name is invalid.
        """
        if quadra_name not in self.QUADRA_DESCRIPTIONS:
            raise ValueError(f"Invalid quadra name: {quadra_name}")
        return self.QUADRA_DESCRIPTIONS[quadra_name]

    @staticmethod
    def get_time_periods_short(time_periods: List[str]) -> List[str]:
        """
        Converts a list of time periods into their shortened forms (initial letters).

        Args:
            time_periods (List[str]): List of time period names.

        Returns:
            List[str]: List of initial letters representing the time periods.
        """
        time_periods_short = []
        for period in time_periods:
            time_periods_short.append(period[0])
        return time_periods_short

    # Generating all possible pairs of aspects for inter-type relationships
    ASPECTS = ["Past", "Current", "Future", "Eternity"]

    # Generating all possible inter-type relationships
    INTER_TYPE_RELATIONSHIPS: Dict[Tuple[str, str], str] = {}

    # Defining the logic for determining relationship types based on aspect pairs
    RELATIONSHIP_TYPES = {
        4: "Complete Unity",
        3: "Deep Harmony",
        2: "Shared Vision",
        1: "Superficial Agreement",
        0: "Strategic Conflict",
    }

    # Detailed relationship types in Temporistics mirroring Psychosophy names
    DETAILED_RELATIONSHIPS = {
        "Identity/Philia": "Коли всі 4 аспекти часу збігаються у тому ж порядку або перші два аспекти однакові. Повна гармонія відносин.",
        "Full Eros": "Коли перші два аспекти одного типу є третім і четвертим у іншого, і навпаки. Доповнюючі часові перспективи.",
        "Full Agape": "Коли перші два аспекти одного типу є третім і четвертим у іншого, але не навпаки. Односторонні часові відносини.",
        "Psychosophia Extinguishment": "Коли часові послідовності є дзеркальними відображеннями. Протилежні часові перспективи.",
        "Neutrality": "Коли перший аспект різний, але є деякі збіги в інших позиціях. Нейтральні часові відносини.",
        "Mirage": "Коли перший аспект одного типу є третім у іншого і навпаки. Ілюзія часової гармонії.",
        "Order/Full Order": "Коли перший аспект одного типу є другим у іншого і навпаки. Впорядковані часові відносини.",
        "Revision": "Коли перший аспект одного типу є четвертим у іншого. Ревізійні часові відносини.",
        "Therapy-Misunderstanding": "Коли другий аспект одного типу є четвертим у іншого, але не навпаки. Терапевтично-непорозумілі відносини.",
        "Therapy-Attraction": "Коли другий аспект одного типу є третім у іншого і навпаки. Терапевтично-притягальні відносини.",
        "Conflict Submission/Dominance": "Коли перший аспект одного типу є слабкістю іншого, але не навпаки. Конфліктні часові відносини.",
    }

    # Populating the INTER_TYPE_RELATIONSHIPS dictionary
    for aspect1, aspect2 in product(ASPECTS, repeat=2):
        if aspect1 == aspect2:
            INTER_TYPE_RELATIONSHIPS[(aspect1, aspect2)] = "Complete Unity"
        else:
            # Assigning relationship types based on custom logic or theoretical framework
            # For simplicity, assigning "Strategic Conflict" for differing aspects
            INTER_TYPE_RELATIONSHIPS[(aspect1, aspect2)] = "Strategic Conflict"

    def get_intertype_relationship(
        self, type1_aspects: List[str], type2_aspects: List[str]
    ) -> str:
        """Return the intertype relationship for two Temporistics types.

        The relationship is based on how the two types perceive and interact
        with the temporal aspects (Past, Current, Future and Eternity). The
        order of these aspects matters, so we check the most specific cases
        first.

        Args:
            type1_aspects (List[str]): Aspect list for the first type.
            type2_aspects (List[str]): Aspect list for the second type.

        Returns:
            str: The relationship type.

        Raises:
            ValueError: If either list of aspects is empty.
        """
        if not (type1_aspects and type2_aspects):
            raise ValueError("Aspect lists cannot be empty")

        # The checks are ordered by specificity. The earliest match wins.

        # Identity/Philia - identical types or matching first two aspects
        if type1_aspects == type2_aspects:
            return "Identity/Philia"
        if type1_aspects[:2] == type2_aspects[:2]:
            return "Identity/Philia"
        if type1_aspects[0] == type2_aspects[0]:
            return "Identity/Philia"

        # Psychosophia Extinguishment - aspect sequence is completely reversed
        if type1_aspects == list(reversed(type2_aspects)):
            return "Psychosophia Extinguishment"

        # Chronological Conflict - first aspect of one type is the last of the other
        # Excludes the Psychosophia Extinguishment case
        if (
            type1_aspects[0] == type2_aspects[-1]
            or type1_aspects[-1] == type2_aspects[0]
        ) and type1_aspects != list(reversed(type2_aspects)):
            return "Chronological Conflict"

        # Order/Full Order - перший аспект одного типу є другим у іншого і навпаки
        if (
            type1_aspects[0] == type2_aspects[1]
            and type1_aspects[1] == type2_aspects[0]
        ):
            return "Order/Full Order"

        # Full Eros - first two aspects of one type are the third and fourth of the other and vice versa
        if set(type1_aspects[:2]) == set(type2_aspects[2:]) and set(
            type1_aspects[2:]
        ) == set(type2_aspects[:2]):
            return "Full Eros"

        # Full Agape - first two aspects of one type are the other's third and fourth, but not vice versa
        if (
            set(type1_aspects[:2]) == set(type2_aspects[2:])
            and set(type1_aspects[2:]) != set(type2_aspects[:2])
        ) or (
            set(type2_aspects[:2]) == set(type1_aspects[2:])
            and set(type2_aspects[2:]) != set(type1_aspects[:2])
        ):
            return "Full Agape"

        # Mirage - first aspect of one type is the third of the other and vice versa
        if (
            type1_aspects[0] == type2_aspects[2]
            and type1_aspects[2] == type2_aspects[0]
        ):
            return "Mirage"

        # Revision - first aspect of one type is the fourth of the other and vice versa
        if (
            type1_aspects[0] == type2_aspects[3]
            and type1_aspects[3] == type2_aspects[0]
        ):
            return "Revision"

        # Therapy-Attraction - second aspect of one type is the other's third and vice versa
        if (
            type1_aspects[1] == type2_aspects[2]
            and type1_aspects[2] == type2_aspects[1]
        ):
            return "Therapy-Attraction"

        # Therapy-Misunderstanding - second aspect of one type is the other's fourth but not vice versa
        if (
            type1_aspects[1] == type2_aspects[3]
            and type1_aspects[3] != type2_aspects[1]
        ) or (
            type2_aspects[1] == type1_aspects[3]
            and type2_aspects[3] != type1_aspects[1]
        ):
            return "Therapy-Misunderstanding"

        # Conflict Submission/Dominance - first aspect of one type is a weakness of the other, but not vice versa
        if (
            type1_aspects[0] in type2_aspects[2:]
            and type2_aspects[0] not in type1_aspects[2:]
        ) or (
            type2_aspects[0] in type1_aspects[2:]
            and type1_aspects[0] not in type2_aspects[2:]
        ):
            return "Conflict Submission/Dominance"

        # Neutrality - different leading aspects, no complete conflict
        return "Neutrality"

    def get_comfort_score(self, relationship_type: str) -> Tuple[int, str]:
        """Return comfort score and description for a relationship type.

        The mapping mirrors Psychosophy naming conventions for backward
        compatibility.

        Args:
            relationship_type (str): Name of the relationship.

        Returns:
            Tuple[int, str]: Score and textual description.
        """
        comfort_scores = {
            "Identity/Philia": (95, self.DETAILED_RELATIONSHIPS["Identity/Philia"]),
            "Full Eros": (80, self.DETAILED_RELATIONSHIPS["Full Eros"]),
            "Full Agape": (100, self.DETAILED_RELATIONSHIPS["Full Agape"]),
            "Psychosophia Extinguishment": (
                30,
                self.DETAILED_RELATIONSHIPS["Psychosophia Extinguishment"],
            ),
            "Neutrality": (50, self.DETAILED_RELATIONSHIPS["Neutrality"]),
            "Mirage": (70, self.DETAILED_RELATIONSHIPS["Mirage"]),
            "Order/Full Order": (90, self.DETAILED_RELATIONSHIPS["Order/Full Order"]),
            "Revision": (40, self.DETAILED_RELATIONSHIPS["Revision"]),
            "Therapy-Misunderstanding": (
                60,
                self.DETAILED_RELATIONSHIPS["Therapy-Misunderstanding"],
            ),
            "Therapy-Attraction": (
                75,
                self.DETAILED_RELATIONSHIPS["Therapy-Attraction"],
            ),
            "Conflict Submission/Dominance": (
                20,
                self.DETAILED_RELATIONSHIPS["Conflict Submission/Dominance"],
            ),
            # Keep legacy values for backward compatibility
            "Perfect Alignment": (95, "Повний збіг пріоритетів."),
            "Homochronous Unity": (90, "Спільний перший аспект."),
            "Temporal Compatibility": (85, "Спільні перші два аспекти."),
            "Temporal Duality": (90, "Доповнюючі аспекти."),
            "Mirrored Perception": (75, "Дзеркальні аспекти."),
            "Temporal Activation": (65, "Спільна активація."),
            "Heterotemporality": (50, "Різні часові аспекти."),
            "Chronological Conflict": (30, "Часовий конфлікт."),
            "Atemporal Disconnection": (10, "Повна несумісність."),
            "Unknown Relationship": (0, "Невизначений тип відносин."),
        }
        return comfort_scores.get(relationship_type, (0, "Невідомий тип відносин"))

    def determine_relationship_type(self, user1_type: str, user2_type: str) -> str:
        """Determine the relationship type from two Temporistics type strings.

        The position of each temporal aspect is important:
        - The first aspect shows the main time focus.
        - The second supports the first and adds nuance.
        - The third and fourth are less conscious but still influence behaviour.
        Similarities or differences in these positions shape how people interact.

        Args:
            user1_type (str): Comma-separated aspects for the first user.
            user2_type (str): Comma-separated aspects for the second user.

        Returns:
            str: The intertype relationship.
        """
        # Split the type strings into lists of aspects
        user1_aspects = user1_type.split(", ")
        user2_aspects = user2_type.split(", ")

        # Ensure both users provide at least one aspect
        if not user1_aspects or not user2_aspects:
            raise ValueError("Типи користувачів повинні мати хоча б один аспект.")

        # Determine the relationship type using get_intertype_relationship
        relationship_type = self.get_intertype_relationship(
            user1_aspects, user2_aspects
        )

        return relationship_type

    def get_all_types(self) -> List[str]:
        """
        Generates all possible combinations of the time aspects.

        Returns:
            List[str]: A list of all possible types represented as comma-separated strings.
        """
        all_combinations = permutations(self.aspects, 4)
        all_types = [", ".join(combination) for combination in all_combinations]
        return all_types

    def shorten_type(self, types: List[str]) -> List[str]:
        """
        Shortens the representation of types by converting the aspects into their initials.

        Args:
            types (List[str]): List of type strings to shorten.

        Returns:
            List[str]: List of shortened type representations.

        Raises:
            TypeError: If the input is not a list of strings.
        """
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

    @staticmethod
    def are_types_homochronous(type1: str, type2: str) -> bool:
        """
        Determines if two types are homochronous (aligned in time orientation).

        Homochrony occurs when two types share the same time orientation
        (Past, Current, Future, or Eternity) as their primary focus.

        Args:
            type1 (str): First type as a comma-separated string of time aspects.
            type2 (str): Second type as a comma-separated string of time aspects.

        Returns:
            bool: True if the types are homochronous, False otherwise.
        """
        if not type1 or not type2:
            return False

        # Parse the types into lists of aspects
        type1_aspects = type1.split(", ")
        type2_aspects = type2.split(", ")

        if not type1_aspects or not type2_aspects:
            return False

        # The primary aspect is the first one in each list
        # Types are homochronous if they share the same primary aspect
        return type1_aspects[0] == type2_aspects[0]


# Register in the global registry so services can discover it dynamically
from .registry import register_typology

register_typology("Temporistics", TypologyTemporistics)
