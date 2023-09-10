from typologies.typology_temporistics import TypologyTemporistics

from typologies.typology_psychosophia import TypologyPsychosophia
from typologies.typology_amatoric import TypologyAmatoric
from typologies.typology_socionics import TypologySocionics
from enum import Enum

class RelationshipType(Enum):
    PHILIA = "Philia"
    PSEUDO_PHILIA = "Pseudo-Philia"
    AGAPE = "Agape"
    FULL_AGAPE = "Full Agape"
    EROS = "Eros"
    EROS_VARIANT = "Eros Variant"
    FULL_EROS = "Full Eros"
    UNKNOWN = "Unknown Relationship"

class RelationshipCalculator:
    """A class to calculate the relationship type and comfort score between two users based on their typology aspects."""

    COMFORT_SCORES = {
        RelationshipType.PHILIA: 5,
        RelationshipType.PSEUDO_PHILIA: 3,
        RelationshipType.AGAPE: 8,
        RelationshipType.FULL_AGAPE: 10,
        RelationshipType.EROS: -2,
        RelationshipType.EROS_VARIANT: -1,
        RelationshipType.FULL_EROS: -5
    }

    # Terminal color codes
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

    def __init__(self, user1, user2, typology):
        """Initialize the class with two users."""
        self.user1 = user1
        self.user2 = user2
        self.typology = typology

    def get_relationship_color(self, comfort_score):
        """Return the color code based on comfort score."""
        if comfort_score > 0:
            return self.GREEN
        elif comfort_score < 0:
            return self.RED
        else:
            return self.YELLOW

    def determine_relationship_type(self):
        """Determine the type of relationship between the two users."""
        if self.user1 == self.user2:
            return RelationshipType.PHILIA

        if (
            (self.user1[1] == self.user2[2] and self.user1[2] == self.user2[1]) and 
            (self.user1[0] == self.user2[3] and self.user1[3] == self.user2[0])
        ):
            return RelationshipType.FULL_AGAPE

        if (
            (self.user1[0] == self.user2[2] or self.user1[2] == self.user2[0]) and
            (self.user1[1] == self.user2[3] or self.user1[3] == self.user2[1])
        ):
            return RelationshipType.FULL_EROS

        if self.user1[0] == self.user2[0] and self.user1[1] == self.user2[2]:
            return RelationshipType.AGAPE

        if self.user1[0] == self.user2[2] or self.user1[2] == self.user2[0]:
            return RelationshipType.EROS

        if self.user1[1] == self.user2[3] or self.user1[3] == self.user2[1]:
            return RelationshipType.EROS_VARIANT

        if (
            (self.user1[0] == self.user2[0] and self.user1[3] == self.user2[3]) or
            (self.user1[1] == self.user2[1] and self.user1[2] == self.user2[2])
        ):
            return RelationshipType.PSEUDO_PHILIA

        return RelationshipType.UNKNOWN

    def get_comfort_score(self, relationship_type):
        """Return the comfort score for the given relationship type."""
        return self.COMFORT_SCORES.get(relationship_type, 0)  # Default to 0 if relationship type is not found

def main():
    available_typologies = {
        "Temporistics": TypologyTemporistics,
        "Psychosophia": TypologyPsychosophia,
        "Amatoric": TypologyAmatoric,
        "Socionics": TypologySocionics
    }

    print("Available typologies:")
    for idx, typology_name in enumerate(available_typologies.keys(), 1):
        print(f"{idx}. {typology_name}")

    selected_typologies_numbers = input("Which typologies do you want to use for compatibility calculation? (e.g., '1,2,3,4' for all): ")
    chosen_numbers = [int(num) for num in selected_typologies_numbers.split(",")]

    # Get the selected typologies based on the chosen numbers
    selected_typologies = [available_typologies[list(available_typologies.keys())[num-1]] for num in chosen_numbers]

    def get_user_type(typology_instance, person="you"):
        # Display available types for the selected typology
        available_types = typology_instance.get_all_types()
        for idx, t in enumerate(available_types, 1):
            print(f"{idx}. {t}")

        # Get type based on user selection
        user_input = input(f"What's {person} type number from the above list? ")
        while not user_input.isdigit() or int(user_input) not in range(1, len(available_types) + 1):
            print("Invalid choice. Please select a valid number.")
            user_input = input(f"What's {person} type number from the above list? ")
        return available_types[int(user_input) - 1]

    # Gather user and partner types for each selected typology
    user_types = {}
    partner_types = {}
    for typology_class in selected_typologies:
        typology_name = typology_class.__name__
        typology_instance = typology_class()

        print(f"\nAvailable types for {typology_name}:")
        user_types[typology_name] = get_user_type(typology_instance, person="you")
        partner_types[typology_name] = get_user_type(typology_instance, person="your partner")

    print("\nYour selected types are:")
    for typology, user_type in user_types.items():
        print(f"{typology} - You: {user_type} | Partner: {partner_types[typology]}")

if __name__ == "__main__":
    main()


