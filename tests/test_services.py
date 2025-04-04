import pytest
from app.services import get_types_by_typology, calculate_relationship
from app import db
from app.models import User, UserType
from tests.test_helpers import unique_username, unique_email
import uuid


@pytest.fixture
def setup_database(app, db_url):
    with app.app_context():
        user_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        db.session.add(user_type)
        db.session.commit()
        email = unique_email("testuser")
        user = User(username=unique_username("testuser"), email=email, user_type=user_type)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
    yield

def test_get_types_by_typology(app, setup_database):
    with app.app_context():
        types = get_types_by_typology("Temporistics")
        assert types is not None
        assert any("Past" in type_string for type_string in types)
        assert any("Future" in type_string for type_string in types)

def test_calculate_relationship(app, setup_database):
    with app.app_context():
        relationship_type, comfort_score = calculate_relationship(
            "Past, Current, Future, Eternity",
            "Current, Past, Future, Eternity",
            "Temporistics"
        )
        assert relationship_type is not None
        assert comfort_score is not None

def test_get_types_psychosophia(app, setup_database):
    with app.app_context():
        types = get_types_by_typology("Psychosophia")
        assert types is not None
        assert len(types) > 0

def test_calculate_relationship_invalid_typology(app, setup_database):
    with app.app_context():
        with pytest.raises(ValueError):
            calculate_relationship("Past", "Future", "NonExistentTypology")

def test_calculate_relationship_empty_input(app, setup_database):
    with app.app_context():
        with pytest.raises(ValueError):
            calculate_relationship("", "Future", "Temporistics")

def test_get_distance_if_compatible(app, setup_database):
    from app.models import User, UserType, db
    from app.services import get_distance_if_compatible
    import pytest

    with app.app_context():
        # Create the initial user type and commit it
        user_type = UserType(
            typology_name="Temporistics",
            type_value="Past, Current, Future, Eternity"
        )
        db.session.add(user_type)
        db.session.commit()

        # Використовуємо унікальні email та username
        unique_id = uuid.uuid4().hex[:8]
        username1 = f"user1_{unique_id}"
        username2 = f"user2_{unique_id}"
        email1 = f"u1_{unique_id}@example.com"
        email2 = f"u2_{unique_id}@example.com"
        
        # Create two users with this user type
        user1 = User(username=username1, email=email1,
                     latitude=40.0, longitude=-73.0, user_type=user_type)
        user1.set_password("pass1")

        user2 = User(username=username2, email=email2,
                     latitude=41.0, longitude=-74.0, user_type=user_type)
        user2.set_password("pass2")

        db.session.add_all([user1, user2])
        db.session.commit()

        # Initially, they should be compatible
        dist = get_distance_if_compatible(user1, user2)
        assert dist > 0

        # Create another user type with a rearranged aspect order resulting in fewer positional matches
        another_type = UserType(
            typology_name="Temporistics",
            type_value="Eternity, Future, Current, Past"
        )
        db.session.add(another_type)
        db.session.commit()

        # Assign the new incompatible user type to user2
        user2.user_type = another_type
        db.session.commit()

        # Now they should have fewer matches => comfort_score <= 50 => ValueError expected
        with pytest.raises(ValueError):
            get_distance_if_compatible(user1, user2)


