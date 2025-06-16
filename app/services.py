import math
from flask import current_app
from .extensions import db, cache
from .typologies import (
    TypologyTemporistics,
    TypologyPsychosophia,
    TypologyAmatoric,
    TypologySocionics,
)

# Central registry for available typologies. This allows us to reuse the same
# mapping across helper functions instead of redefining it in each place.
TYPOLOGY_CLASSES = {
    "Temporistics": TypologyTemporistics,
    "Psychosophia": TypologyPsychosophia,
    "Amatoric": TypologyAmatoric,
    "Socionics": TypologySocionics,
}

def get_types_by_typology(typology_name):
    """Отримання всіх типів для заданої типології.
    У тестовому середовищі не використовує кешування."""
    typology_class = TYPOLOGY_CLASSES.get(typology_name)
    if not typology_class:
        return None
    
    # Перевіряємо, чи знаходимося в тестовому середовищі
    if current_app.config.get('TESTING', False) or current_app.config.get('CACHE_TYPE') == 'NullCache':
        return typology_class().get_all_types()
    else:
        # Використовуємо кешування лише в не-тестовому середовищі
        return _get_types_cached(typology_name, typology_class)

@cache.memoize(timeout=3600)  # Cache the result for 1 hour
def _get_types_cached(typology_name, typology_class):
    """Кешована версія отримання типів."""
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


def create_user_type(typology_name, type_value, commit=True):
    """Create a new ``UserType`` instance and optionally commit it."""
    from .models import UserType
    user_type = UserType(
        typology_name=typology_name,
        type_value=type_value,
    )
    db.session.add(user_type)
    if commit:
        db.session.commit()
    else:
        # Ensure ID is available without committing the whole transaction
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

def update_user_profile(user, username, email, typology_name, type_value, latitude, longitude,
                        city=None, country=None, profession=None, profession_visible=None, max_distance=None):
    user.username = username
    user.email = email
    assign_user_type(user, typology_name, type_value, commit=False)

    user.latitude = latitude
    user.longitude = longitude
    if city is not None:
        user.city = city
    if country is not None:
        user.country = country
    if profession is not None:
        user.profession = profession
    if profession_visible is not None:
        user.profession_visible = profession_visible
    
    # Оновлюємо максимальну прийнятну відстань, якщо вона вказана
    if max_distance is not None:
        user.max_distance = max_distance
    
    db.session.commit()

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad)*math.cos(lat2_rad)*math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def get_users_distance(user1, user2):
    if user1.latitude is None or user1.longitude is None or user2.latitude is None or user2.longitude is None:
        raise ValueError("Both users must have coordinates set")
    return haversine_distance(user1.latitude, user1.longitude, user2.latitude, user2.longitude)

def get_distance_if_compatible(user1, user2):
    from .services import calculate_relationship
    if user1.user_type is None or user2.user_type is None:
        raise ValueError("Both users must have a user_type assigned")
    relationship_type, comfort_score = calculate_relationship(user1.user_type.type_value, user2.user_type.type_value, user1.user_type.typology_name)
    if comfort_score <= 50:
        raise ValueError("Users are not compatible enough to consider meeting")
    
    # Отримуємо відстань між користувачами
    distance = get_users_distance(user1, user2)
    
    # Перевіряємо, чи відстань не перевищує максимальну прийнятну відстань для першого користувача
    if user1.max_distance is not None and distance > user1.max_distance:
        raise ValueError(f"User is too far away (distance: {distance:.2f} km, max: {user1.max_distance:.2f} km)")
    
    return distance

def get_typology_instance(typology_name):
    typology_class = TYPOLOGY_CLASSES.get(typology_name)
    if typology_class is None:
        return None
    return typology_class()
