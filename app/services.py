import math
from flask import current_app
from .extensions import db, cache
from .typologies import (
    TypologyTemporistics,
    TypologyPsychosophia,
    TypologyAmatoric,
    TypologySocionics,
    TypologyIQ,
)

# Central registry for available typologies. This allows us to reuse the same
# mapping across helper functions instead of redefining it in each place.
TYPOLOGY_CLASSES = {
    "Temporistics": TypologyTemporistics,
    "Psychosophia": TypologyPsychosophia,
    "Amatoric": TypologyAmatoric,
    "Socionics": TypologySocionics,
    "IQ": TypologyIQ,
}
"""Compatibility layer for service functions."""

from .domain_services import (
    get_types_by_typology,
    calculate_relationship,
    haversine_distance,
    get_users_distance,
    get_distance_if_compatible,
    get_typology_instance,
)



from .repositories.user_repository import update_user_profile

__all__ = [
    "get_types_by_typology",
    "calculate_relationship",
    "haversine_distance",
    "get_users_distance",
    "get_distance_if_compatible",
    "get_typology_instance",
    "update_user_profile",
]

