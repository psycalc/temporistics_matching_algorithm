from abc import ABC

class Type(ABC):

    def __init__(self, full_name: str, pseudonym: str):
        self._full_name = full_name
        self._pseudonym = pseudonym
        self._short_name = self._generate_short_name()

    @property
    def full_name(self) -> str:
        """Get the full name of the type."""
        return self._full_name

    @property
    def short_name(self) -> str:
        """Get the short name of the type."""
        return self._short_name

    @property
    def pseudonym(self) -> str:
        """Get the pseudonym of the type."""
        return self._pseudonym

    def _generate_short_name(self) -> str:
        """Generate the short name based on the full name."""
        return "".join(word[0] for word in self._full_name.split())
