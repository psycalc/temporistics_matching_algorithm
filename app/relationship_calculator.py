import json
import os
from enum import Enum
from .typologies.typology_temporistics import TypologyTemporistics
from .typologies.typology_psychosophia import TypologyPsychosophia
from .typologies.typology_amatoric import TypologyAmatoric
from .typologies.typology_socionics import TypologySocionics
from .typologies.typology_iq import TypologyIQ


# Function to load relationship data from a JSON file
def load_relationship_data(file_path):
    """Load relationship data from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing the relationship data.

    Returns:
        dict: The loaded relationship data.
    """
    # Adjust the path according to the placement of your JSON file within your project structure
    base_dir = os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )  # This navigates up to the project root
    full_path = os.path.join(
        base_dir, "data", file_path
    )  # Assumes the JSON is under the 'data' directory
    with open(full_path, "r") as file:
        data = json.load(file)
    return data


class RelationshipType(Enum):
    # Socionics Relationships
    IDENTITY = "Identity"
    DUALITY = "Duality"
    ACTIVITY = "Activity"
    MIRROR = "Mirror"
    KINDRED = "Kindred"
    SEMI_DUALITY = "Semi-duality"
    BUSINESS = "Business"
    ILLUSIONARY = "Illusionary"
    SUPER_EGO = "Super-ego"
    CONTRARY = "Contrary"
    QUASI_IDENTITY = "Quasi-identity"
    EXTINGUISHMENT = "Extinguishment"
    CONFLICT = "Conflict"
    BENEFIT = "Benefit"

    # Temporistics Relationships (базові)
    HOMOCHRONY = "Homochrony"
    HETEROCHRONY = "Heterochrony"
    
    # Temporistics Relationships (деталізовані)
    PERFECT_ALIGNMENT = "Perfect Alignment"
    HOMOCHRONOUS_UNITY = "Homochronous Unity"
    TEMPORAL_COMPATIBILITY = "Temporal Compatibility"
    TEMPORAL_DUALITY = "Temporal Duality"
    MIRRORED_PERCEPTION = "Mirrored Perception"
    TEMPORAL_ACTIVATION = "Temporal Activation"
    HETEROTEMPORALITY = "Heterotemporality"
    CHRONOLOGICAL_CONFLICT = "Chronological Conflict"
    ATEMPORAL_DISCONNECTION = "Atemporal Disconnection"

    # Psychosophia Relationships
    IDENTITY_PHILIA = "Identity/Philia"
    FULL_EROS = "Full Eros"
    FULL_AGAPE = "Full Agape"
    PSYCHOSOPHIA_EXTINGUISHMENT = "Psychosophia Extinguishment"  # Renamed
    NEUTRALITY = "Neutrality"
    MIRAGE = "Mirage"
    ORDER_FULL_ORDER = "Order/Full Order"
    REVISION = "Revision"
    THERAPY_MISUNDERSTANDING = "Therapy-Misunderstanding"
    THERAPY_ATTRACTION = "Therapy-Attraction"
    CONFLICT_SUBMISSION_DOMINANCE = "Conflict Submission/Dominance"

    # Amatoric Relationships
    PHILIA = "Philia"
    STORGE = "Storge"
    EROS = "Eros"
    AGAPE = "Agape"

    UNKNOWN = "Unknown Relationship"


class RelationshipCalculator:
    """Class to calculate the relationship type and comfort score based on typology aspects."""

    def __init__(self, user1, user2, typology):
        self.user1 = user1
        self.user2 = user2
        self.typology = typology
        self.load_comfort_scores()

    def load_comfort_scores(self):
        """Load comfort scores from a JSON file."""
        self.COMFORT_SCORES = load_relationship_data(
            f"{self.typology.lower()}_comfort_scores.json"
        )

    def get_relationship_color(self, comfort_score):
        """Return the color code based on comfort score."""
        if comfort_score > 0:
            return "\033[92m"  # Green
        elif comfort_score < 0:
            return "\033[91m"  # Red
        return "\033[93m"  # Yellow

    def determine_relationship_type(self):
        """Determine the relationship type based on user types and typology.

        Returns:
            RelationshipType: The determined relationship type.
        """
        user1_type = self.user1.type
        user2_type = self.user2.type

        if self.typology == "Socionics":
            # Socionics relationship determination logic
            if user1_type == user2_type:
                return RelationshipType.IDENTITY
            elif user1_type == TypologySocionics.get_dual_type(user2_type):
                return RelationshipType.DUALITY
            elif user1_type == TypologySocionics.get_activity_type(user2_type):
                return RelationshipType.ACTIVITY
            # Add more conditions for other Socionics relationship types
            else:
                return RelationshipType.UNKNOWN

        elif self.typology == "Temporistics":
            # Temporistics relationship determination logic
            temporistics = TypologyTemporistics()
            relationship_type_str = temporistics.determine_relationship_type(user1_type, user2_type)
            
            # Повертаємо відповідний RelationshipType на основі рядка
            relationship_mapping = {
                "Perfect Alignment": RelationshipType.PERFECT_ALIGNMENT,
                "Homochronous Unity": RelationshipType.HOMOCHRONOUS_UNITY,
                "Temporal Compatibility": RelationshipType.TEMPORAL_COMPATIBILITY,
                "Temporal Duality": RelationshipType.TEMPORAL_DUALITY,
                "Mirrored Perception": RelationshipType.MIRRORED_PERCEPTION,
                "Temporal Activation": RelationshipType.TEMPORAL_ACTIVATION,
                "Heterotemporality": RelationshipType.HETEROTEMPORALITY,
                "Chronological Conflict": RelationshipType.CHRONOLOGICAL_CONFLICT,
                "Atemporal Disconnection": RelationshipType.ATEMPORAL_DISCONNECTION,
            }
            
            return relationship_mapping.get(relationship_type_str, RelationshipType.UNKNOWN)

        elif self.typology == "Psychosophia":
            # Psychosophia relationship determination logic
            psychosophia_typology = TypologyPsychosophia()
            if psychosophia_typology.are_types_identity_philia(user1_type, user2_type):
                return RelationshipType.IDENTITY_PHILIA
            elif psychosophia_typology.are_types_full_eros(user1_type, user2_type):
                return RelationshipType.FULL_EROS
            elif psychosophia_typology.are_types_full_agape(user1_type, user2_type):
                return RelationshipType.FULL_AGAPE
            elif psychosophia_typology.are_types_extinguishment(user1_type, user2_type):
                return RelationshipType.PSYCHOSOPHIA_EXTINGUISHMENT
            elif psychosophia_typology.are_types_neutrality(user1_type, user2_type):
                return RelationshipType.NEUTRALITY
            elif psychosophia_typology.are_types_mirage(user1_type, user2_type):
                return RelationshipType.MIRAGE
            elif psychosophia_typology.are_types_order_full_order(
                user1_type, user2_type
            ):
                return RelationshipType.ORDER_FULL_ORDER
            elif psychosophia_typology.are_types_revision(user1_type, user2_type):
                return RelationshipType.REVISION
            elif psychosophia_typology.are_types_therapy_misunderstanding(
                user1_type, user2_type
            ):
                return RelationshipType.THERAPY_MISUNDERSTANDING
            elif psychosophia_typology.are_types_therapy_attraction(
                user1_type, user2_type
            ):
                return RelationshipType.THERAPY_ATTRACTION
            elif psychosophia_typology.are_types_conflict_submission_dominance(
                user1_type, user2_type
            ):
                return RelationshipType.CONFLICT_SUBMISSION_DOMINANCE
            else:
                return RelationshipType.UNKNOWN

        elif self.typology == "Amatoric":
            # Amatoric relationship determination logic
            amatoric_typology = TypologyAmatoric()
            if amatoric_typology.are_types_philia(user1_type, user2_type):
                return RelationshipType.PHILIA
            elif amatoric_typology.are_types_storge(user1_type, user2_type):
                return RelationshipType.STORGE
            elif amatoric_typology.are_types_eros(user1_type, user2_type):
                return RelationshipType.EROS
            elif amatoric_typology.are_types_agape(user1_type, user2_type):
                return RelationshipType.AGAPE
            else:
                return RelationshipType.UNKNOWN

        else:
            return RelationshipType.UNKNOWN

    def get_comfort_score(self, relationship_type):
        """Retrieve the comfort score and description for a given relationship type.

        Args:
            relationship_type (RelationshipType): The type of relationship.

        Returns:
            tuple: The score and description for the relationship type.
        """
        # Fetches the relationship data, defaulting to (0, "Unknown Relationship") if not found
        relationship_data = self.COMFORT_SCORES.get(
            relationship_type.value, {"score": 0, "description": "Unknown Relationship"}
        )
        return (relationship_data["score"], relationship_data["description"])


def main():
    # Example usage
    available_typologies = {
        "Temporistics": TypologyTemporistics(),
        "Psychosophia": TypologyPsychosophia(),
        "Amatoric": TypologyAmatoric(),
        "Socionics": TypologySocionics(),
        "IQ": TypologyIQ(),
    }
    print("Available typologies:")
    for idx, typology_name in enumerate(available_typologies.keys(), start=1):
        print(f"{idx}. {typology_name}")

    # Prompt user for input
    typology_choice = int(input("Enter the number of the desired typology: "))
    typology_name = list(available_typologies.keys())[typology_choice - 1]
    user1_type = input("Enter User 1 Type: ")
    user2_type = input("Enter User 2 Type: ")

    # Create RelationshipCalculator instance and determine relationship type
    user1 = type("User1", (), {"type": user1_type})
    user2 = type("User2", (), {"type": user2_type})
    calculator = RelationshipCalculator(user1, user2, typology_name)
    relationship_type = calculator.determine_relationship_type()
    comfort_score = calculator.get_comfort_score(relationship_type)

    # Display the results
    print(f"Relationship Type: {relationship_type.value}")
    print(f"Comfort Score: {comfort_score[0]}")
    print(f"Description: {comfort_score[1]}")


if __name__ == "__main__":
    main()
