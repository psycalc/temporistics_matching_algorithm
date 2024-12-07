import json
import os
from .relationship_calculator import RelationshipCalculator


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


class SocionicsRelationshipCalculator(RelationshipCalculator):
    # Load relationship data from an external JSON file for easier modification and extension
    SOCIONICS_RELATIONSHIPS = load_relationship_data("socionics_relationships.json")

    def determine_relationship_type(self, user1_type, user2_type):
        """Dynamically determine the relationship type based on user types.

        Args:
            user1_type (str): Type of the first user.
            user2_type (str): Type of the second user.

        Returns:
            str: The determined relationship type.
        """
        # Placeholder logic - replace with your actual logic to determine the relationship type based on Socionics theory
        if user1_type == user2_type:
            return "Identity"
        # Add more logic based on Socionics theory...
        return "Unknown"  # Default case if no type matches

    def get_comfort_score(self, relationship_type):
        """Retrieve the comfort score and description for a given relationship type.

        Args:
            relationship_type (str): The type of relationship.

        Returns:
            tuple: The score and description for the relationship type.
        """
        # Fetches the relationship data, defaulting to (0, "Unknown Relationship") if not found
        relationship_data = self.SOCIONICS_RELATIONSHIPS.get(
            relationship_type, {"score": 0, "description": "Unknown Relationship"}
        )
        return (relationship_data["score"], relationship_data["description"])
