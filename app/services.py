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
    if not user1 or not user2:
        raise ValueError("User types cannot be empty")
    typology_classes = {
        "Temporistics": TypologyTemporistics,
        "Psychosophia": TypologyPsychosophia,
        "Amatoric": TypologyAmatoric,
        "Socionics": TypologySocionics,
    }
    typology_class = typology_classes.get(typology)
    if typology_class is None:
        raise ValueError(f"Invalid typology: {typology}")
    typology_instance = typology_class()
    
    relationship_type = typology_instance.determine_relationship_type(user1, user2)
    comfort_score, _ = typology_instance.get_comfort_score(relationship_type)
    return relationship_type, comfort_score
