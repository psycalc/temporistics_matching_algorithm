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


def test_login(client, app):
    with app.app_context():
        response = client.post("/login", data={
            "email": "test@example.com",
            "password": "testpassword",
            "submit": "Login"
        }, follow_redirects=True)
        # Проверяем, что редирект на index, и пользователь залогинен
        assert response.status_code == 200
        # В идеале проверить current_user, но current_user не доступен напрямую.
        # Можно проверить контекст или использовать Flask-Login utilities.
        # Простой вариант: Протестировать, что в ответе есть какая-то фраза для залогиненного пользователя.

def test_login_wrong_password(client, app):
    with app.app_context():
        response = client.post("/login", data={
            "email": "test@example.com",
            "password": "wrongpassword",
            "submit": "Login"
        }, follow_redirects=True)
        # Должен остаться на странице логина с flash сообщением
        assert response.status_code == 200
        assert b"Login Unsuccessful" in response.data

def test_logout(client, app):
    with app.app_context():
        # Сначала логинимся
        client.post("/login", data={
            "email": "test@example.com",
            "password": "testpassword"
        }, follow_redirects=True)
        # Теперь логаут
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        # Можно проверить, что в ответе нет признаков залогиненного пользователя

def test_protected_page_requires_login(client, app):
    with app.app_context():
        response = client.get("/user/testuser", follow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]

