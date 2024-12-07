from abc import ABC, abstractmethod

class Typology(ABC):
    def __init__(self, aspects):
        self.aspects = aspects

    @abstractmethod
    def get_all_types(self):
        pass

    @abstractmethod
    def shorten_type(self, types):
        pass

    @abstractmethod
    def determine_relationship_type(self, user1_type: str, user2_type: str) -> str:
        """
        Определяет тип отношений между двумя типами.
        """
        pass

    @abstractmethod
    def get_comfort_score(self, relationship_type: str) -> (int, str):
        """
        Возвращает кортеж (числовой_скор_комфорта, текстовое_описание) для данного типа отношений.
        """
        pass
