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
