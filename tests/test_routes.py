import pytest
import uuid
from app import db
from app.models import User, UserType
from flask_login import current_user

def unique_username(prefix="testuser"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def unique_email(prefix="test", domain="example.com"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@{domain}"

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 302

def test_login(client, app):
    with app.app_context():
        username = unique_username("loginuser")
        email = unique_email("loginuser")
        user = User(username=username, email=email)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()

        response = client.post("/login", data={
            "email": email,
            "password": "testpassword",
            "submit": "Login"
        }, follow_redirects=True)
        assert response.status_code == 200
        # Можно добавить дополнительные проверки содержимого ответа, если нужно.

        # Можно проверить признаки успешной авторизации, например, наличие ссылки на logout или profile.

def test_login_wrong_password(client, app):
    with app.app_context():
        username = unique_username("wrongpass")
        email = unique_email("wrongpass")  # используем функцию для уникального email
        user = User(username=username, email=email)
        user.set_password("correctpassword")
        db.session.add(user)
        db.session.commit()

    response = client.post("/login", data={
        "email": email,
        "password": "wrongpassword",
        "submit": "Login"
    }, follow_redirects=True)

    print(response.data)
    assert response.status_code == 200
    assert b"Login Unsuccessful" in response.data



def test_logout(client, app):
    with app.app_context():
        username = unique_username("logoutuser")
        email = unique_email("logoutuser")
        user = User(username=username, email=email)
        user.set_password("testpassword3")
        db.session.add(user)
        db.session.commit()

        client.post("/login", data={
            "email": email,
            "password": "testpassword3"
        }, follow_redirects=True)

        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200

def test_protected_page_requires_login(client, app):
    # Проверим, что если не залогинены, нас редиректит на /login
    # Возможно, ваш код сейчас редиректит на "/", это надо исправить в приложении.
    # Предположим, что мы хотим редирект на "/login". Если реально приложение редиректит на "/",
    # скорректируйте тест так, чтобы ожидать "/".
    response = client.get("/user/someusername", follow_redirects=False)
    # Если приложение корректно настроено, незалогиненный юзер при попытке доступа должен редиректиться на /login
    assert response.status_code == 302
    location = response.headers.get("Location", "")
    # Убедимся, что действительно редирект на "/login"
    # Если ваш код сейчас редиректит на "/", нужно либо исправить приложение, либо тест.
    assert "/login" in location, f"Expected redirect to /login, got {location}"

def test_edit_profile_route(client, app):
    with app.app_context():
        username = unique_username("editprofile")
        email = unique_email("editprofile")
        user = User(username=username, email=email)
        user.set_password("testpassword4")
        db.session.add(user)
        db.session.commit()

        client.post('/login', data={
            'email': email,
            'password': 'testpassword4'
        }, follow_redirects=True)

        response = client.get('/edit_profile', follow_redirects=True)
        assert response.status_code == 200
        assert b"Edit Profile" in response.data

        new_username = unique_username("new_user")
        new_email = unique_email("new_email")

        response = client.post('/edit_profile', data={
            'username': new_username,
            'email': new_email,
            'typology_name': 'Updated Typology',
            'type_value': 'Updated Value',
            'latitude': '40.0',
            'longitude': '-73.0'
        }, follow_redirects=True)

        assert b"Profile updated successfully." in response.data

        # Дополнительная проверка: извлечь обновленного пользователя из БД
        updated_user = User.query.filter_by(id=user.id).first()
        assert updated_user is not None
        assert updated_user.username == new_username
        assert updated_user.email == new_email
        # Если вы храните поля latitude/longitude в модели User,
        # То стоит проверить и их, например:
        assert updated_user.latitude == 40.0
        assert updated_user.longitude == -73.0

        # Также проверяем типологию
        updated_type = updated_user.user_type
        assert updated_type is not None
        assert updated_type.typology_name == 'Updated Typology'
        assert updated_type.type_value == 'Updated Value'


def test_compatible_nearby_link_visibility(client, app):
    # Проверяем, что без авторизации ссылка не отображается
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Compatible Nearby" not in response.data

    # Логинимся
    with app.app_context():
        # Предполагаем, что у нас есть пользователь "testuser" (создан в setup_database)
        response = client.post("/login", data={
            "email": "test@example.com",
            "password": "testpassword",
            "submit": "Login"
        }, follow_redirects=True)
        assert response.status_code == 200
        # Теперь проверяем, что ссылка на Compatible Nearby появилась
        response = client.get("/", follow_redirects=True)
        assert b"Compatible Nearby" in response.data

def test_nearby_compatibles_page(client, app):
    # Логин
    with app.app_context():
        response = client.post("/login", data={
            "email": "test@example.com",
            "password": "testpassword",
            "submit": "Login"
        }, follow_redirects=True)
        assert response.status_code == 200

        # Заходим на страницу nearby_compatibles
        response = client.get("/nearby_compatibles", follow_redirects=True)
        assert response.status_code == 200
        # Проверяем что страница отобразилась без ошибок
        # Можно проверить по наличию каких-то ключевых слов
        # Например, если шаблон содержит фразу "Compatible Users Nearby:"
        assert b"Compatible Users Nearby:" in response.data

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

