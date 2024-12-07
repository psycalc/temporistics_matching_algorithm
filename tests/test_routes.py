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
        # Заменяем "YourTypeValue" на действительный тип
        user_type = UserType(
            typology_name="Temporistics",
            type_value="Past, Current, Future, Eternity"
        )
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
        assert response.status_code == 200
        # Можно добавить дополнительные проверки содержимого ответа, если нужно.


def test_login_wrong_password(client, app):
    with app.app_context():
        response = client.post("/login", data={
            "email": "test@example.com",
            "password": "wrongpassword",
            "submit": "Login"
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b"Login Unsuccessful" in response.data


def test_logout(client, app):
    with app.app_context():
        client.post("/login", data={
            "email": "test@example.com",
            "password": "testpassword"
        }, follow_redirects=True)
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200


def test_protected_page_requires_login(client, app):
    with app.app_context():
        response = client.get("/user/testuser", follow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.headers["Location"]

def test_get_types(client, app):
    with app.app_context():
        response = client.get("/get_types?typology=Temporistics")
        assert response.status_code == 200
        data = response.get_json()
        assert "types" in data
        assert any("Past" in t for t in data["types"])

def test_calculate(client, app):
    with app.app_context():
        # Валидный запрос
        response = client.post("/calculate", data={
            "user1": "Past, Current, Future, Eternity",
            "user2": "Past, Current, Future, Eternity",
            "typology": "Temporistics"
        })
        assert response.status_code == 200
        assert b"result.html" not in response.data # Шаблон не обязательно упомянут в контенте, но можно проверить контент.
        assert b"Comfort Score:" in response.data

        # Невалидный запрос, например без user2
        response = client.post("/calculate", data={
            "user1": "Past, Current, Future, Eternity",
            "typology": "Temporistics"
        })
        # Проверяем, что все равно 200, но контент другой или flash сообщение (в зависимости от реализации)
        assert response.status_code == 200

def test_change_language(client, app):
    with app.app_context():
        # Валидный язык
        response = client.post("/change_language", data={"language": "en"}, follow_redirects=False)
        assert response.status_code == 302
        assert "locale" in response.headers.get("Set-Cookie", "")
        # Невалидный язык
        response = client.post("/change_language", data={"language": "xx"}, follow_redirects=True)
        assert response.status_code == 400
        assert b"Language change failed" in response.data

def test_register_get(client, app):
    with app.app_context():
        response = client.get("/register")
        assert response.status_code == 200
        assert b"Register" in response.data

def test_register_post_valid(client, app):
    with app.app_context():
        response = client.post("/register", data={
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword",
            "confirm_password": "newpassword",
            "typologies-0-typology_name": "Temporistics",
            "typologies-0-type_value": "Past, Current, Future, Eternity",
            "typologies-1-typology_name": "Psychosophia",
            "typologies-1-type_value": "Emotion, Logic, Will, Physics",
            "typologies-2-typology_name": "Amatoric",
            "typologies-2-type_value": "Love, Passion, Friendship, Romance",
            "typologies-3-typology_name": "Socionics",
            "typologies-3-type_value": "Intuitive, Ethical, Extratim"  # или любой доступный тип
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b"Your account has been created! You can now log in." in response.data
        # Проверить в базе, что user создан
        new_user = User.query.filter_by(username="newuser").first()
        assert new_user is not None

def test_register_post_invalid(client, app):
    with app.app_context():
        # Уже есть testuser, попробуем зарегать второго с тем же email
        response = client.post("/register", data={
            "username": "testuser2",
            "email": "test@example.com",
            "password": "newpassword",
            "confirm_password": "newpassword"
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b"Registration failed" in response.data

def test_user_profile_logged_in(client, app):
    with app.app_context():
        # Логинимся
        client.post("/login", data={
            "email": "test@example.com",
            "password": "testpassword"
        }, follow_redirects=True)
        # Смотрим свой профиль
        response = client.get("/user/testuser")
        assert response.status_code == 200
        assert b"test@example.com" in response.data # email в форме
        # Пробуем изменить профиль
        response = client.post("/user/testuser", data={
            "email": "updated@example.com",
            "typology_name": "Temporistics",
            "type_value": "Past, Current, Future, Eternity"
        }, follow_redirects=True)
        assert response.status_code == 200
        updated_user = User.query.filter_by(username="testuser").first()
        assert updated_user.email == "updated@example.com"

def test_user_profile_other_user(client, app):
    with app.app_context():
        client.post("/login", data={
            "email": "test@example.com",
            "password": "testpassword"
        }, follow_redirects=True)
        # Пытаемся зайти на профиль другого пользователя, которого нет
        response = client.get("/user/nonexistentuser")
        assert response.status_code == 404

