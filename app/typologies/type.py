from abc import ABC, abstractmethod
from typing import Dict

class Type(ABC):
    """
    An abstract base class for different psychological types.
    This class provides a structure for defining various attributes and behaviors common to all types.
    """

    def __init__(self, full_name: str, pseudonym: str, aspect: str, descriptions: Dict[str, Dict[str, str]]):
        """
        Initializes a new instance of a Type.

        :param full_name: The full name of the type.
        :param pseudonym: A shorthand or alternative name.
        :param aspect: The main aspect or characteristic of the type.
        :param descriptions: A dictionary containing descriptions of the type.
        """
        self._full_name = full_name
        self._pseudonym = pseudonym
        self._aspect = aspect
        self._descriptions = descriptions
        self._short_name = self._generate_short_name()

    @property
    def full_name(self) -> str:
        """Returns the full name of the type."""
        return self._full_name

    @property
    def short_name(self) -> str:
        """Returns the short name of the type."""
        return self._short_name

    @property
    def pseudonym(self) -> str:
        """Returns the pseudonym of the type."""
        return self._pseudonym

    @property
    def aspect(self) -> str:
        """Returns the main aspect of the type."""
        return self._aspect

    @property
    def descriptions(self) -> Dict[str, str]:
        """Returns the descriptions of the type."""
        return self._descriptions

    def _generate_short_name(self) -> str:
        """Generates a short name based on the full name of the type."""
        return "".join(word[0].upper() for word in self._full_name.split())

    @abstractmethod
    def get_description(self, length: str = 'short') -> str:
        """
        Abstract method to get a description of the type.
        Must be implemented by subclasses to return either a short or full description.

        :param length: The length of the description ('short' or 'full').
        :return: The requested description of the type.
        """
        pass
