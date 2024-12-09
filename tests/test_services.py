import pytest
from app.services import get_types_by_typology, calculate_relationship
from app import db
from app.models import User, UserType

@pytest.fixture(autouse=True)
def setup_database(app, db_url):
    with app.app_context():
        user_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        db.session.add(user_type)
        db.session.commit()
        user = User(username="testuser", email="test@example.com", user_type=user_type)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
    yield

def test_get_types_by_typology(app):
    with app.app_context():
        types = get_types_by_typology("Temporistics")
        assert types is not None
        assert any("Past" in type_string for type_string in types)
        assert any("Future" in type_string for type_string in types)

def test_calculate_relationship(app):
    with app.app_context():
        relationship_type, comfort_score = calculate_relationship(
            "Past", "Future", "Temporistics"
        )
        assert relationship_type is not None
        assert comfort_score is not None

def test_get_types_psychosophia(app):
    with app.app_context():
        types = get_types_by_typology("Psychosophia")
        assert types is not None
        assert len(types) > 0

def test_calculate_relationship_invalid_typology(app):
    with app.app_context():
        with pytest.raises(ValueError):
            calculate_relationship("Past", "Future", "NonExistentTypology")

def test_calculate_relationship_empty_input(app):
    with app.app_context():
        with pytest.raises(ValueError):
            calculate_relationship("", "Future", "Temporistics")

def test_get_distance_if_compatible(app):
    from app.models import User, UserType, db
    from app.services import get_distance_if_compatible
    with app.app_context():
        user_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        db.session.add(user_type)
        db.session.commit()

        user1 = User(username="user1", email="u1@example.com", latitude=40.0, longitude=-73.0, user_type=user_type)
        user1.set_password("pass1")
        user2 = User(username="user2", email="u2@example.com", latitude=41.0, longitude=-74.0, user_type=user_type)
        user2.set_password("pass2")
        db.session.add_all([user1, user2])
        db.session.commit()

        dist = get_distance_if_compatible(user1, user2)
        assert dist > 0

        another_type = UserType(typology_name="Temporistics", type_value="Past")
        db.session.add(another_type)
        db.session.commit()

        user2.user_type = another_type
        db.session.commit()

        import pytest
        with pytest.raises(ValueError):
            get_distance_if_compatible(user1, user2)
