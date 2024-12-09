from .extensions import db, cache
from .typologies import (
    TypologyTemporistics,
    TypologyPsychosophia,
    TypologyAmatoric,
    TypologySocionics,
)


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
