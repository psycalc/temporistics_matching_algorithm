from app.extensions import db


def update_user_profile(
    user,
    username,
    email,
    typology_name,
    type_value,
    latitude,
    longitude,
    city=None,
    country=None,
    profession=None,
    profession_visible=None,
    max_distance=None,
):
    """Update user profile information and commit to the database."""
    user.username = username
    user.email = email

    if user.user_type:
        user.user_type.typology_name = typology_name
        user.user_type.type_value = type_value
    else:
        from app.models import UserType

        user_type = UserType(typology_name=typology_name, type_value=type_value)
        db.session.add(user_type)
        db.session.commit()
        user.type_id = user_type.id

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

    if max_distance is not None:
        user.max_distance = max_distance

    db.session.commit()

    return user

