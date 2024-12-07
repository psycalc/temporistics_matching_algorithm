import pytest
from app import db
from app.models import User, UserType


@pytest.fixture(autouse=True)
def setup_database(app, db_url):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    with app.app_context():
        db.create_all()
    yield
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_user_model(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username="testuser").first()
        assert retrieved_user is not None
        assert retrieved_user.email == "test@example.com"
        assert retrieved_user.check_password("testpassword")


def test_user_with_type(app):
    with app.app_context():
        # Создаём UserType
        user_type = UserType(typology_name="Temporistics", type_value="SomeValue")
        db.session.add(user_type)
        db.session.commit()

        # Создаём User с user_type
        user = User(username="typeuser", email="type@example.com", user_type=user_type)
        user.set_password("securepass")
        db.session.add(user)
        db.session.commit()

        retrieved = User.query.filter_by(username="typeuser").first()
        assert retrieved is not None
        assert retrieved.user_type is not None
        assert retrieved.user_type.typology_name == "Temporistics"
        assert retrieved.user_type.type_value == "SomeValue"

def test_user_uniqueness(app):
    with app.app_context():
        user1 = User(username="uniqueuser", email="unique@example.com")
        user1.set_password("pass1")
        db.session.add(user1)
        db.session.commit()

        user2 = User(username="uniqueuser", email="unique2@example.com")
        user2.set_password("pass2")
        db.session.add(user2)
        # Ожидаем, что при commit будет ошибка уникальности
        # В реальности вы можете ожидать IntegrityError от SQLAlchemy:
        import sqlalchemy.exc
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            db.session.commit()

