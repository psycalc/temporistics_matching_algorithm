import pytest
from app import db
from app.models import User, UserType
from flask_login import current_user


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def setup_database(app, db_url):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    with app.app_context():
        db.create_all()
        user_type = UserType(typology_name="Temporistics", type_value="YourTypeValue")
        db.session.add(user_type)
        db.session.commit()
        user = User(username="testuser", email="test@example.com", user_type=user_type)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
    yield
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 302


# Змініть інші тести аналогічним чином
