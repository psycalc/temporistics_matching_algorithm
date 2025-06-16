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
    "create_user_type",
    "assign_user_type",
]


def create_user_type(typology_name, type_value, commit=True):
    """Create a :class:`~app.models.UserType` and optionally commit it."""
    from .models import UserType

    user_type = UserType(
        typology_name=typology_name,
        type_value=type_value,
    )
    db.session.add(user_type)
    if commit:
        db.session.commit()
    else:
        # Ensure the new ``id`` is available for further use without committing
        db.session.flush()
    return user_type


def assign_user_type(user, typology_name, type_value, commit=True):
    """Assign or update ``user.user_type`` with the provided values."""
    if user.user_type:
        user.user_type.typology_name = typology_name
        user.user_type.type_value = type_value
    else:
        user_type = create_user_type(typology_name, type_value, commit=False)
        user.type_id = user_type.id
    if commit:
        db.session.commit()

