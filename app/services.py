"""Compatibility layer for service functions."""

from .domain_services import (
    get_types_by_typology,
    calculate_relationship,
    haversine_distance,
    get_users_distance,
    get_distance_if_compatible,
    get_typology_instance,
)

# update_user_profile is now located in app.repositories.user_repository
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
