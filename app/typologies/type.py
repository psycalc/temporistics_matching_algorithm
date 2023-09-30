from abc import ABC
from typing import Dict

class Type(ABC):

    def __init__(self, full_name: str, pseudonym: str, aspect: str, descriptions: Dict[str, Dict[str, str]]):
        self._full_name = full_name
        self._pseudonym = pseudonym
        self._short_name = self._generate_short_name()
        self._aspect = aspect
        self._short_description = self._generate_description(descriptions, 'short')
        self._full_description = self._generate_description(descriptions, 'full')

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def short_name(self) -> str:
        return self._short_name

    @property
    def pseudonym(self) -> str:
        return self._pseudonym

    @property
    def short_description(self) -> str:
        return self._short_description

    @property
    def full_description(self) -> str:
        return self._full_description

    def _generate_short_name(self) -> str:
        return "".join(word[0] for word in self._full_name.split())

    def _generate_description(self, descriptions: Dict[str, Dict[str, str]], desc_type: str) -> str:
        return descriptions.get(self._aspect, {}).get(desc_type, '')
