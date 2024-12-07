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


# Змініть інші тести аналогічним чином
