from flask_caching import Cache
from .typologies import (
    TypologyTemporistics,
    TypologyPsychosophia,
    TypologyAmatoric,
    TypologySocionics,
)

cache = Cache()  # Initialize Cache without passing the app instance


@cache.memoize(timeout=3600)  # Cache the result for 1 hour
def get_types_by_typology(typology_name):
    typology_classes = {
        "Temporistics": TypologyTemporistics,
        "Psychosophia": TypologyPsychosophia,
        "Amatoric": TypologyAmatoric,
        "Socionics": TypologySocionics,
    }
    typology_class = typology_classes.get(typology_name)
    if not typology_class:
        return None
    return typology_class().get_all_types()


def calculate_relationship(user1, user2, typology):
    # Dynamically select the typology class based on the input
    typology_classes = {
        "Temporistics": TypologyTemporistics,
        "Psychosophia": TypologyPsychosophia,
        "Amatoric": TypologyAmatoric,
        "Socionics": TypologySocionics,
    }

    # Instantiate the typology class
    typology_instance = typology_classes.get(typology)()
    if not typology_instance:
        raise ValueError(f"Invalid typology: {typology}")

    # Determine the relationship type using the selected typology class
    relationship_type = typology_instance.determine_relationship_type(user1, user2)

    # Calculate the comfort score for the determined relationship type
    comfort_score, _ = typology_instance.get_comfort_score(relationship_type)

    return relationship_type, comfort_score
