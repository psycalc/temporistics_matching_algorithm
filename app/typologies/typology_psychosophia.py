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
        """Парсить рядок типу у список аспектів"""
        if not type_str:
            return []
        return type_str.split(", ")

    def are_types_identity_philia(self, type1: List[str], type2: List[str]) -> bool:
        """
        Перевіряє, чи є відносини між типами ідентичністю/філією.
        Це відбувається, коли типи ідентичні або коли перші дві функції однакові.
        """
        return type1 == type2 or type1[:2] == type2[:2]

    def are_types_extinguishment(self, type1: List[str], type2: List[str]) -> bool:
        """
        Перевіряє, чи є відносини між типами погашенням.
        Це відбувається, коли типи мають повністю протилежний порядок функцій.
        """
        return type1 == list(reversed(type2))

    def are_types_full_eros(self, type1: List[str], type2: List[str]) -> bool:
        """
        Перевіряє, чи є відносини між типами повним еросом.
        Це відбувається, коли перші дві функції одного типу є третьою і четвертою в іншого, І НАВПАКИ.
        Відносини не повинні бути Extinguishment або Identity.
        """
        if self.are_types_extinguishment(type1, type2) or type1 == type2:
             return False
        
        # Умова 1: Перші два type1 = Останні два type2
        cond1 = set(type1[:2]) == set(type2[2:])
        # Умова 2: Останні два type1 = Перші два type2
        cond2 = set(type1[2:]) == set(type2[:2])
        
        # Ерос вимагає, щоб ОБИДВІ умови виконувались
        return cond1 and cond2

    def are_types_full_agape(self, type1: List[str], type2: List[str]) -> bool:
        """
        Перевіряє, чи є відносини між типами повною агапе.
        Це відбувається, коли перші дві функції одного типу є третьою і четвертою в іншого, АЛЕ НЕ навпаки.
        Відносини не повинні бути Extinguishment, Eros або Identity.
        """
        if self.are_types_extinguishment(type1, type2) or type1 == type2:
            return False
            
        # Умова 1: Перші два type1 = Останні два type2
        cond1 = set(type1[:2]) == set(type2[2:])
        # Умова 2: Останні два type1 = Перші два type2
        cond2 = set(type1[2:]) == set(type2[:2])
        
        # Випадок Ероса (обидві умови істинні)
        is_eros = cond1 and cond2
        
        # Агапе вимагає, щоб виконувалась лише одна з умов (XOR) І це не був випадок Ероса
        # Враховуючи, що ми вже перевірили на Eros у determine_relationship_type, 
        # достатньо перевірити, чи виконується хоча б одна умова, АЛЕ НЕ обидві.
        return (cond1 or cond2) and not is_eros

    def are_types_order_full_order(self, type1: List[str], type2: List[str]) -> bool:
        """
        Перевіряє, чи є відносини між типами порядком/повним порядком.
        Це відбувається, коли перша функція одного типу є другою в іншого і навпаки.
        """
        return type1[0] == type2[1] and type1[1] == type2[0]

    def are_types_mirage(self, type1: List[str], type2: List[str]) -> bool:
        """
        Перевіряє, чи є відносини між типами міражем.
        Це відбувається, коли перша функція одного типу є третьою в іншого і навпаки.
        """
        return type1[0] == type2[2] and type1[2] == type2[0]

    def are_types_revision(self, type1: List[str], type2: List[str]) -> bool:
        """
        Перевіряє, чи є відносини між типами ревізією.
        Це відбувається, коли перша функція одного типу є четвертою в іншого і навпаки.
        """
        return type1[0] == type2[3] and type1[3] == type2[0]

    def are_types_therapy_attraction(self, type1: List[str], type2: List[str]) -> bool:
        """
        Перевіряє, чи є відносини між типами терапією-притягненням.
        Це відбувається, коли друга функція одного типу є третьою в іншого і навпаки.
        """
        return type1[1] == type2[2] and type1[2] == type2[1]

    def are_types_therapy_misunderstanding(self, type1: List[str], type2: List[str]) -> bool:
        """
        Перевіряє, чи є відносини між типами терапією-непорозумінням.
        Це відбувається, коли друга функція одного типу є четвертою в іншого, але не навпаки.
        """
        cond1 = type1[1] == type2[3] and type1[3] != type2[1]
        cond2 = type2[1] == type1[3] and type2[3] != type1[1]
        return cond1 or cond2 # Implicit XOR, as both true would imply Extinguishment in some cases (e.g. 1234 vs 4321)

    def are_types_conflict_submission_dominance(self, type1: List[str], type2: List[str]) -> bool:
        """
        Перевіряє, чи є відносини між типами конфліктом підкорення/домінування.
        Це відбувається, коли перша функція одного типу є слабкістю іншого (3 або 4 позиція), але не навпаки.
        """
        # Видалено спеціальний випадок
        cond1 = type1[0] in type2[2:] and type2[0] not in type1[2:]
        cond2 = type2[0] in type1[2:] and type1[0] not in type2[2:]
        return cond1 or cond2 # Implicit XOR logic

    def determine_relationship_type(self, user1_type: str, user2_type: str) -> str:
        """
        Визначає тип відносин між двома користувачами на основі їхніх типів Психософії.
        Порядок перевірок критичний для уникнення неоднозначності.
        """
        user1_aspects = self._parse_type_to_list(user1_type)
        user2_aspects = self._parse_type_to_list(user2_type)
        
        if not user1_aspects or not user2_aspects or len(user1_aspects) != 4 or len(user2_aspects) != 4:
            return "Unknown Relationship" # Basic validation
            
        # Перевірка валідності аспектів (можна додати, якщо потрібно)
        # all_aspects_valid = all(aspect in self.aspects for aspect in user1_aspects + user2_aspects)
        # if not all_aspects_valid:
        #     return "Unknown Relationship"
                
        # 1. Ідентичність/Філія
        if self.are_types_identity_philia(user1_aspects, user2_aspects):
            return "Identity/Philia"
        
        # 2. Погашення
        if self.are_types_extinguishment(user1_aspects, user2_aspects):
            return "Psychosophia Extinguishment"
            
        # 3. Повний Ерос
        if self.are_types_full_eros(user1_aspects, user2_aspects):
            return "Full Eros"
            
        # 4. Повна Агапе
        if self.are_types_full_agape(user1_aspects, user2_aspects):
            return "Full Agape"
            
        # 5. Порядок/Повний порядок
        if self.are_types_order_full_order(user1_aspects, user2_aspects):
            return "Order/Full Order"
            
        # 6. Міраж
        if self.are_types_mirage(user1_aspects, user2_aspects):
            return "Mirage"
            
        # 7. Ревізія
        if self.are_types_revision(user1_aspects, user2_aspects):
            return "Revision"
            
        # 8. Терапія-Притягнення
        if self.are_types_therapy_attraction(user1_aspects, user2_aspects):
            return "Therapy-Attraction"
            
        # 9. Терапія-Непорозуміння
        if self.are_types_therapy_misunderstanding(user1_aspects, user2_aspects):
            return "Therapy-Misunderstanding"
            
        # 10. Конфлікт Підкорення/Домінування
        if self.are_types_conflict_submission_dominance(user1_aspects, user2_aspects):
            return "Conflict Submission/Dominance"
            
        # 11. Нейтралітет (якщо жодна з попередніх умов не виконалась)
        return "Neutrality"

    def get_comfort_score(self, relationship_type: str) -> (int, str):
        """
        Повертає оцінку комфорту та опис для даного типу відносин.
        
        Args:
            relationship_type (str): Тип відносин
            
        Returns:
            tuple: (оцінка_комфорту, опис)
        """
        comfort_scores = {
            "Identity/Philia": (9, "Взаємодія легка, комфортна і дружня"),
            "Full Eros": (8, "Взаємодія динамічна, стимулююча і сповнена взаємного інтересу"),
            "Full Agape": (10, "Взаємодія комфортна, гармонійна і взаємовигідна"),
            "Psychosophia Extinguishment": (-5, "Взаємодія віддалена, формальна з взаємоповагою"),
            "Neutrality": (0, "Взаємодія нейтральна і ввічлива, але без глибокого розуміння"),
            "Mirage": (3, "Взаємодія непередбачувана, інтенсивна і емоційно заряджена"),
            "Order/Full Order": (6, "Взаємодія асиметрична, один партнер більш активний і домінуючий"),
            "Revision": (-3, "Взаємодія складна і конфронтаційна, але може вести до росту"),
            "Therapy-Misunderstanding": (2, "Взаємодія комфортна і легка через спільні цінності"),
            "Therapy-Attraction": (4, "Взаємодія асиметрична, один партнер більш активний і підтримуючий"),
            "Conflict Submission/Dominance": (-4, "Взаємодія характеризується боротьбою за владу і конфліктами")
        }
        
        return comfort_scores.get(
            relationship_type, 
            (0, "Невідомий тип відносин")
        )
