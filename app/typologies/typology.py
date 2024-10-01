from abc import ABC, abstractmethod

class Typology(ABC):

    def __init__(self, aspects):
        self.aspects = aspects

    @abstractmethod
    def get_all_types(self):
        """
        Абстрактный метод, который должен возвращать все типы для данной типологии.
        """
        pass

    @abstractmethod
    def shorten_type(self, types):
        """
        Абстрактный метод, который сокращает типы в случае необходимости.
        """
        pass

    @staticmethod
    def get_typology_classes():
        """
        Возвращает список всех классов-наследников типологии.
        Это позволяет динамически находить и использовать любые типологии.
        """
        return Typology.__subclasses__()