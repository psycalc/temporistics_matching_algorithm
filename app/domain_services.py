from haversine import haversine, Unit
from flask import current_app
from .extensions import cache
from .typologies.registry import get_typology_classes


# Central registry for available typologies loaded from the registry.
TYPOLOGY_CLASSES = get_typology_classes()


def get_types_by_typology(typology_name):
    """Retrieve all types for a given typology.
    In testing environments caching is skipped."""
    typology_class = TYPOLOGY_CLASSES.get(typology_name)
    if not typology_class:
        return None

    if (
        current_app.config.get("TESTING", False)
        or current_app.config.get("CACHE_TYPE") == "NullCache"
    ):
        return typology_class().get_all_types()
    else:
        return _get_types_cached(typology_name, typology_class)


@cache.memoize(timeout=3600)
def _get_types_cached(typology_name, typology_class):
    """Cached version of get_types_by_typology."""
    return typology_class().get_all_types()


def calculate_relationship(user1, user2, typology):
    if not user1 or not user2:
        raise ValueError("User types cannot be empty")
    typology_class = TYPOLOGY_CLASSES.get(typology)
    if typology_class is None:
        raise ValueError(f"Invalid typology: {typology}")
    typology_instance = typology_class()
    relationship_type = typology_instance.determine_relationship_type(user1, user2)
    comfort_score, _ = typology_instance.get_comfort_score(relationship_type)
    return relationship_type, comfort_score


def get_users_distance(user1, user2):
    """Return the distance between two users based on their coordinates."""
    if (
        user1.latitude is None
        or user1.longitude is None
        or user2.latitude is None
        or user2.longitude is None
    ):
        raise ValueError("Both users must have coordinates set")
    return haversine(
        (user1.latitude, user1.longitude),
        (user2.latitude, user2.longitude),
        unit=Unit.KILOMETERS,
    )


def get_distance_if_compatible(user1, user2):
    if user1.user_type is None or user2.user_type is None:
        raise ValueError("Both users must have a user_type assigned")
    relationship_type, comfort_score = calculate_relationship(
        user1.user_type.type_value,
        user2.user_type.type_value,
        user1.user_type.typology_name,
    )
    if comfort_score <= 50:
        raise ValueError("Users are not compatible enough to consider meeting")

    distance = get_users_distance(user1, user2)

    if user1.max_distance is not None and distance > user1.max_distance:
        raise ValueError(
            f"User is too far away (distance: {distance:.2f} km, max: {user1.max_distance:.2f} km)"
        )

    return distance


def get_typology_instance(typology_name):
    typology_class = TYPOLOGY_CLASSES.get(typology_name)
    if typology_class is None:
        return None
    return typology_class()
