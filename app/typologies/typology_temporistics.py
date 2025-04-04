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

    # Деталізовані типи відносин у Temporistics з назвами як у Психософії
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
        "Conflict Submission/Dominance": "Коли перший аспект одного типу є слабкістю іншого, але не навпаки. Конфліктні часові відносини."
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
        Визначає тип міжтипових відносин для двох типів на основі їх аспектів.
        
        Відносини визначаються тим, як різні типи сприймають і взаємодіють з часовими перспективами.
        Важливим є порядок часових аспектів (минуле, теперішнє, майбутнє, вічність), 
        оскільки це впливає на характер взаємодії.

        Args:
            type1_aspects (List[str]): Список аспектів для першого типу.
            type2_aspects (List[str]): Список аспектів для другого типу.

        Returns:
            str: Тип міжтипових відносин.

        Raises:
            ValueError: Якщо списки аспектів не є дійсними.
        """
        if not (type1_aspects and type2_aspects):
            raise ValueError("Списки аспектів не можуть бути порожніми.")

        # Порядок перевірок має значення!
        # Спочатку перевіряємо найбільш специфічні випадки

        # Identity/Philia - ідентичні типи або однакові перші два аспекти або спільний перший аспект
        if type1_aspects == type2_aspects:
            return "Identity/Philia"
        if type1_aspects[:2] == type2_aspects[:2]:
            return "Identity/Philia"
        if type1_aspects[0] == type2_aspects[0]:
            return "Identity/Philia"
            
        # Психосоphia Extinguishment - повністю протилежні послідовності часових аспектів
        if type1_aspects == list(reversed(type2_aspects)):
            return "Psychosophia Extinguishment"
            
        # Chronological Conflict - перший аспект одного типу є останнім у іншого
        # Виключаємо випадок Psychosophia Extinguishment
        if (type1_aspects[0] == type2_aspects[-1] or type1_aspects[-1] == type2_aspects[0]) and type1_aspects != list(reversed(type2_aspects)):
            return "Chronological Conflict"
            
        # Order/Full Order - перший аспект одного типу є другим у іншого і навпаки
        if type1_aspects[0] == type2_aspects[1] and type1_aspects[1] == type2_aspects[0]:
            return "Order/Full Order"
            
        # Full Eros - перші дві функції одного типу є третьою і четвертою в іншого, і навпаки
        if set(type1_aspects[:2]) == set(type2_aspects[2:]) and set(type1_aspects[2:]) == set(type2_aspects[:2]):
            return "Full Eros"
            
        # Full Agape - перші дві функції одного типу є третьою і четвертою в іншого, але не навпаки
        if ((set(type1_aspects[:2]) == set(type2_aspects[2:]) and set(type1_aspects[2:]) != set(type2_aspects[:2])) or
           (set(type2_aspects[:2]) == set(type1_aspects[2:]) and set(type2_aspects[2:]) != set(type1_aspects[:2]))):
            return "Full Agape"
            
        # Mirage - перша функція одного типу є третьою в іншого і навпаки
        if type1_aspects[0] == type2_aspects[2] and type1_aspects[2] == type2_aspects[0]:
            return "Mirage"
            
        # Revision - перша функція одного типу є четвертою в іншого і навпаки
        if type1_aspects[0] == type2_aspects[3] and type1_aspects[3] == type2_aspects[0]:
            return "Revision"
            
        # Therapy-Attraction - друга функція одного типу є третьою в іншого і навпаки
        if type1_aspects[1] == type2_aspects[2] and type1_aspects[2] == type2_aspects[1]:
            return "Therapy-Attraction"
            
        # Therapy-Misunderstanding - друга функція одного типу є четвертою в іншого, але не навпаки
        if ((type1_aspects[1] == type2_aspects[3] and type1_aspects[3] != type2_aspects[1]) or
            (type2_aspects[1] == type1_aspects[3] and type2_aspects[3] != type1_aspects[1])):
            return "Therapy-Misunderstanding"
            
        # Conflict Submission/Dominance - перша функція одного типу є слабкістю іншого, але не навпаки
        if ((type1_aspects[0] in type2_aspects[2:] and type2_aspects[0] not in type1_aspects[2:]) or
            (type2_aspects[0] in type1_aspects[2:] and type1_aspects[0] not in type2_aspects[2:])):
            return "Conflict Submission/Dominance"
            
        # Neutrality - різні перші функції, немає повного конфлікту
        return "Neutrality"

    def get_comfort_score(self, relationship_type: str) -> Tuple[int, str]:
        """
        Повертає оцінку комфорту та опис для даного типу відносин,
        використовуючи нові назви відносин за аналогією з Психософією.

        Args:
            relationship_type (str): Тип відносин.

        Returns:
            Tuple[int, str]: Кортеж, що містить оцінку комфорту та її опис.
        """
        comfort_scores = {
            "Identity/Philia": (95, self.DETAILED_RELATIONSHIPS["Identity/Philia"]),
            "Full Eros": (80, self.DETAILED_RELATIONSHIPS["Full Eros"]),
            "Full Agape": (100, self.DETAILED_RELATIONSHIPS["Full Agape"]),
            "Psychosophia Extinguishment": (30, self.DETAILED_RELATIONSHIPS["Psychosophia Extinguishment"]),
            "Neutrality": (50, self.DETAILED_RELATIONSHIPS["Neutrality"]),
            "Mirage": (70, self.DETAILED_RELATIONSHIPS["Mirage"]),
            "Order/Full Order": (90, self.DETAILED_RELATIONSHIPS["Order/Full Order"]),
            "Revision": (40, self.DETAILED_RELATIONSHIPS["Revision"]),
            "Therapy-Misunderstanding": (60, self.DETAILED_RELATIONSHIPS["Therapy-Misunderstanding"]),
            "Therapy-Attraction": (75, self.DETAILED_RELATIONSHIPS["Therapy-Attraction"]),
            "Conflict Submission/Dominance": (20, self.DETAILED_RELATIONSHIPS["Conflict Submission/Dominance"]),
            
            # Зберігаємо старі значення для зворотної сумісності
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
        """
        Визначає тип відносин між двома користувачами на основі їхніх часових аспектів.
        
        В Темпористиці, порядок часових аспектів є критичним для визначення 
        типу взаємодії між людьми:
        
        - Перший аспект визначає основний фокус уваги і сприйняття часу
        - Другий аспект підтримує перший і визначає додатковий акцент
        - Третій і четвертий аспекти є менш свідомими, але важливими для повного розуміння типу
        
        Отже, збіги або відмінності в цих аспектах визначають характер взаємодії.

        Args:
            user1_type (str): Розділений комами рядок часових аспектів для першого користувача.
            user2_type (str): Розділений комами рядок часових аспектів для другого користувача.

        Returns:
            str: Тип міжтипових відносин.
        """
        # Розділяємо рядки на списки аспектів
        user1_aspects = user1_type.split(", ")
        user2_aspects = user2_type.split(", ")

        # Перевіряємо, чи обидва користувачі мають визначені аспекти
        if not user1_aspects or not user2_aspects:
            raise ValueError("Типи користувачів повинні мати хоча б один аспект.")

        # Визначаємо тип відносин, використовуючи метод get_intertype_relationship
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
