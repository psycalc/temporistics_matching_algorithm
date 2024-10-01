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
        '6-1-2': "Era of Individuality (P)",
        '2-3-4': "Era of Order (E)",
        '4-5-6': "Era of Movement (F)",
        '1-5-3': "Golden Age of Each Era (C)"
    }

    # Dictionary containing quadras with their types and descriptions.
    QUADRAS_AND_DESCRIPTIONS: Dict[str, Dict[str, List[str]]] = {
        'Antipodes': {
            'types': ["Game Master", "Maestro", "Player", "Politician"],
            'description': 'Antipodes are one-plane C and P. Fixed position in all senses, focused on self-image and manipulation.'
        },
        'Guardians and Border Guards': {
            'types': ["Missionary", "Standard Bearer", "Rescuer", "Knight"],
            'description': 'Guardians and Border Guards are one-plane F and P. Focused on self-image and the search for place, with manipulation.'
        },
        'Old-timers and Founders': {
            'types': ["Theorist", "Oracle", "Conqueror", "Star"],
            'description': 'Old-timers and Founders are one-plane C and F. Fixed place and existence with manipulation.'
        },
        'Conductors': {
            'types': ["Ideologist", "Samurai", "Colonist", "Pioneer"],
            'description': 'Conductors are one-plane E and F. Fixed direction and existence, with manipulation.'
        },
        'Scouts': {
            'types': ["Scout", "Hacker", "Gray Cardinal", "Taster"],
            'description': 'Scouts are one-plane C and E. Fixed place and development with manipulation.'
        },
        'Nomads and Tramps': {
            'types': ["Tamada", "Pathfinder", "Robinson", "Initiator"],
            'description': 'Nomads and Tramps are one-plane P and E. Self-image and development are fixed; existence is manipulated.'
        }
    }

    # Separate dictionaries for quadras and their descriptions.
    QUADRAS: Dict[str, List[str]] = {
        quadra_name: data['types'] for quadra_name, data in QUADRAS_AND_DESCRIPTIONS.items()
    }

    QUADRA_DESCRIPTIONS: Dict[str, str] = {
        quadra_name: data['description'] for quadra_name, data in QUADRAS_AND_DESCRIPTIONS.items()
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
        0: "Strategic Conflict"
    }

    # Populating the INTER_TYPE_RELATIONSHIPS dictionary
    for aspect1, aspect2 in product(ASPECTS, repeat=2):
        if aspect1 == aspect2:
            INTER_TYPE_RELATIONSHIPS[(aspect1, aspect2)] = "Complete Unity"
        else:
            # Assigning relationship types based on custom logic or theoretical framework
            # For simplicity, assigning "Strategic Conflict" for differing aspects
            INTER_TYPE_RELATIONSHIPS[(aspect1, aspect2)] = "Strategic Conflict"

    def get_intertype_relationship(self, type1_aspects: List[str], type2_aspects: List[str]) -> str:
        """
        Determines the intertype relationship between two types based on their aspects.

        Args:
            type1_aspects (List[str]): List of aspects for the first type.
            type2_aspects (List[str]): List of aspects for the second type.

        Returns:
            str: The type of intertype relationship.

        Raises:
            ValueError: If the aspects lists are not valid.
        """
        if not (type1_aspects and type2_aspects):
            raise ValueError("Aspects lists cannot be empty.")

        # Counting the number of matching aspects in the same positions
        matches = sum(1 for a1, a2 in zip(type1_aspects, type2_aspects) if a1 == a2)

        # Determining the relationship type based on the number of matches
        relationship_type = self.RELATIONSHIP_TYPES.get(matches, "Unknown Relationship")

        return relationship_type

    def get_comfort_score(self, relationship_type: str) -> Tuple[int, str]:
        """
        Returns a comfort score and description based on the relationship type.

        Args:
            relationship_type (str): The type of relationship.

        Returns:
            Tuple[int, str]: A tuple containing the comfort score and its description.
        """
        comfort_scores = {
            "Complete Unity": (100, "Perfect alignment in all priorities."),
            "Deep Harmony": (90, "Top three time priorities match, leading to significant harmony."),
            "Shared Vision": (75, "Top two priorities align, resulting in cooperation."),
            "Superficial Agreement": (50, "Only one priority matches, leading to shallow agreement."),
            "Strategic Conflict": (25, "Differences lead to friction, but can stimulate growth."),
            "Unknown Relationship": (0, "Relationship type is undefined.")
        }
        return comfort_scores.get(relationship_type, (0, "Unknown relationship type"))

    def determine_relationship_type(self, user1_type: str, user2_type: str) -> str:
        """
        Determines the relationship type between two users based on their time aspects.

        Args:
            user1_type (str): Comma-separated string of time aspects for the first user.
            user2_type (str): Comma-separated string of time aspects for the second user.

        Returns:
            str: The type of intertype relationship.
        """
        user1_aspects = user1_type.split(", ")
        user2_aspects = user2_type.split(", ")

        # Ensuring both users have aspects defined
        if not user1_aspects or not user2_aspects:
            raise ValueError("User types must have at least one aspect.")

        # Determining the relationship type
        relationship_type = self.get_intertype_relationship(user1_aspects, user2_aspects)

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
            initials = ''.join([aspect[0] for aspect in type_name.split(", ")])
            shortened_types.append(initials)
        return shortened_types
