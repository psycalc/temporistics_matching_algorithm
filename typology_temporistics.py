from typing import List
from typology import Typology

class TypologyTemporistics(Typology):
    def __init__(self):
        """
        Initializes a new instance of the TypologyTemporistics class.
        """
        super().__init__(["Past", "Present", "Future", "Eternity"])

    TETRADS = {
        '6-1-2': "Era of Individuality (P)",
        '2-3-4': "Era of Order (E)",
        '4-5-6': "Era of Movement (F)",
        '1-5-3': "Golden Age of Every Era (N)"
    }

    QUADRAS_AND_DESCRIPTIONS = {
        'Antipodes': {
            'types': ["Game Master", "Maestro", "Player", "Politician"],
            'description': 'Antipodes are one-plane N and P. The place is fixed, the position in space is fixed in all senses, the point of view. Everything personal, self-image is fixed. The direction of development and the search for a way of existence are subject to manipulation.'
        },
        'Guardians and Border Guards': {
            'types': ["Missionary", "Standard Bearer", "Rescuer", "Knight"],
            'description': 'Guardians and border guards are one-plane V and P. Everything personal, self-image is fixed. The way to exist is fixed. The direction of development and the search for your place are subject to manipulation.'
        },
        'Old-timers and Founders': {
            'types': ["Theorist", "Oracle", "Conqueror", "Star"],
            'description': 'Old-timers and founders of the “face” world are one-plane N and V. The way to exist is fixed. The place in the world is fixed. The direction of development and everything personal + self-image are subject to manipulation.'
        },
        'Conductors': {
            'types': ["Ideologist", "Samurai", "Colonist", "Pioneer"],
            'description': 'Conductors are one-plane B and V. The way to exist is fixed. The direction of development is fixed. The place in the world and the image of personality are subject to manipulation.'
        },
        'Scouts and Scouts': {
            'types': ["Scout", "Hacker", "Gray Cardinal", "Taster"],
            'description': 'Scouts and scouts are one-plane N and B. The place in the world and the direction of development are fixed. The way to exist and the image of personality are subject to manipulation.'
        },
        'Nomads and Tramps': {
            'types': ["Tamada", "Pathfinder", "Robinson", "Initiator"],
            'description': 'Nomads and tramps are one-plane P and B. Everything personal, self-image, and direction of development are fixed. Place in the world and way of existence are subject to manipulation.'
        }
    }

    def validate_tetrad_sequence(self, tetrad_sequence: str) -> None:
      """
      Validates a tetrad sequence.

      :param tetrad_sequence: A string representing a tetrad sequence.
      :raises ValueError: If the tetrad sequence is invalid.
      """
      if tetrad_sequence not in self.TETRADS:
          raise ValueError(f"Invalid tetrad sequence: {tetrad_sequence}")

    def get_tetrads(self, tetrad_sequence: str) -> str:
      """
      Returns the description for a given tetrad sequence.

      :param tetrad_sequence: A string representing a tetrad sequence.
      :return: A string representing the description for the given tetrad sequence.
      :raises ValueError: If the tetrad sequence is invalid.
      """
      self.validate_tetrad_sequence(tetrad_sequence)
      return self.TETRADS.get(tetrad_sequence, "Unknown Tetrad")

    def get_quadras(self, quadra_name: str) -> List[str]:
      """
      Returns the list of descriptions for a given quadra.

      :param quadra_name: A string representing a quadra name.
      :return: A list of strings representing the descriptions for the given quadra.
      :raises ValueError: If the quadra name is invalid.
      """
      if quadra_name not in self.QUADRAS:
          raise ValueError(f"Invalid quadra name: {quadra_name}")
      return self.QUADRAS[quadra_name]

    def get_quadra_description(self, quadra_name: str) -> str:
      """
      Returns the description for a given quadra.

      :param quadra_name: A string representing a quadra name.
      :return: A string representing the description for the given quadra.
      :raises ValueError: If the quadra name is invalid.
      """
      if quadra_name not in self.QUADRA_DESCRIPTIONS:
          raise ValueError(f"Invalid quadra name: {quadra_name}")
      return self.QUADRA_DESCRIPTIONS[quadra_name]
    
    @staticmethod
    def get_time_periods_short(time_periods: List[str]) -> List[str]:
        """
        Returns the shortened form of the time periods.

        :param time_periods: A list of strings representing the time periods.
        :return: A list of strings representing the shortened form of the time periods.
        """
        time_periods_short = []
        for period in time_periods:
            if period == "Present":
                period = "Current"
            time_periods_short.append(period[0])
        return time_periods_short
