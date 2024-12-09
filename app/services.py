from .extensions import db, cache
from .typologies import (
    TypologyTemporistics,
    TypologyPsychosophia,
    TypologyAmatoric,
    TypologySocionics,
)
import math

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

def update_user_profile(user, username, email, typology_name, type_value, latitude, longitude):
    user.username = username
    user.email = email
    
    if user.user_type:
        user.user_type.typology_name = typology_name
        user.user_type.type_value = type_value
    else:
        from app.models import UserType
        user_type = UserType(
            typology_name=typology_name, 
            type_value=type_value
        )
        db.session.add(user_type)
        db.session.commit()
        user.type_id = user_type.id

    # Здесь, если нужно, можно добавить логику проверки корректности lat/long,
    # или, например, сделать поля latitude/longitude атрибутами пользователя,
    # если они есть в модели User (в коде выше нет таких колонок).
    # Предположим, что они есть в модели User:
    user.latitude = latitude
    user.longitude = longitude

    db.session.commit()

def haversine_distance(lat1, lon1, lat2, lon2):
    # Радиус Земли в км
    R = 6371.0  
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad)*math.cos(lat2_rad)*math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Функция для поиска расстояния между двумя пользователями:
def get_users_distance(user1, user2):
    if user1.latitude is None or user1.longitude is None or user2.latitude is None or user2.longitude is None:
        raise ValueError("Both users must have coordinates set")
    return haversine_distance(user1.latitude, user1.longitude, user2.latitude, user2.longitude)


def get_distance_if_compatible(user1, user2):
    from .services import calculate_relationship
    # Предположим user1_type и user2_type берём из user.user_type.type_value и user.user_type.typology_name
    if user1.user_type is None or user2.user_type is None:
        raise ValueError("Both users must have a user_type assigned")

    relationship_type, comfort_score = calculate_relationship(user1.user_type.type_value, user2.user_type.type_value, user1.user_type.typology_name)
    if comfort_score <= 50:
        raise ValueError("Users are not compatible enough to consider meeting")

    return get_users_distance(user1, user2)

def get_typology_instance(typology_name):
    typology_classes = {
        "Temporistics": TypologyTemporistics,
        "Psychosophia": TypologyPsychosophia,
        "Amatoric": TypologyAmatoric,
        "Socionics": TypologySocionics,
    }
    typology_class = typology_classes.get(typology_name)
    if typology_class:
        return typology_class()
    return None

