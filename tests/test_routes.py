import pytest
from app import db
from app.models import User, UserType
from flask_login import current_user
from tests.test_helpers import unique_username, unique_email
from io import BytesIO
import uuid


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

def test_login_wrong_password(client, app):
    with app.app_context():
        username = unique_username("wrongpass")
        email = unique_email("wrongpass")
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
    response = client.get("/user/someusername", follow_redirects=False)
    assert response.status_code == 302
    location = response.headers.get("Location", "")
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
            'typology_name': 'Temporistics',
            'type_value': 'Past, Current, Future, Eternity',
            'latitude': '40.0',
            'longitude': '-73.0'
        }, follow_redirects=True)
        assert b"Profile updated successfully." in response.data

        updated_user = User.query.filter_by(id=user.id).first()
        assert updated_user is not None
        assert updated_user.username == new_username
        assert updated_user.email == new_email
        assert updated_user.latitude == 40.0
        assert updated_user.longitude == -73.0
        updated_type = updated_user.user_type
        assert updated_type is not None
        assert updated_type.typology_name == 'Temporistics'
        assert updated_type.type_value == 'Past, Current, Future, Eternity'

def test_compatible_nearby_link_visibility(client, app):
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Compatible Nearby" not in response.data

    with app.app_context():
        # Create the user before trying to log in
        username = unique_username("testuser")
        email = unique_email("testuser")
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

        response = client.get("/", follow_redirects=True)
        assert b"Compatible Nearby" in response.data

def test_nearby_compatibles_page(client, app):
    with app.app_context():
        # Create the user before trying to log in
        username = unique_username("testuser")
        email = unique_email("testuser")
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

        response = client.get("/nearby_compatibles", follow_redirects=True)
        assert response.status_code == 200
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
        response = client.post("/calculate", data={
            "user1": "Past, Current, Future, Eternity",
            "user2": "Past, Current, Future, Eternity",
            "typology": "Temporistics"
        })
        assert response.status_code == 200
        assert b"result.html" not in response.data
        assert b"Comfort Score:" in response.data

        response = client.post("/calculate", data={
            "user1": "Past, Current, Future, Eternity",
            "typology": "Temporistics"
        })
        assert response.status_code == 200

def test_change_language(client, app):
    with app.app_context():
        response = client.post("/change_language", data={"language": "en"}, follow_redirects=False)
        assert response.status_code == 302
        assert "locale" in response.headers.get("Set-Cookie", "")

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
        # Використовуємо унікальні значення
        unique_id = uuid.uuid4().hex[:8]
        username = f"newuser_{unique_id}"
        email = f"new_{unique_id}@example.com"
        
        response = client.post("/register", data={
            "username": username,
            "email": email,
            "password": "newpassword",
            "confirm_password": "newpassword",
            "typologies-0-typology_name": "Temporistics",
            "typologies-0-type_value": "Past, Current, Future, Eternity",
            "typologies-1-typology_name": "Psychosophia",
            "typologies-1-type_value": "Emotion, Logic, Will, Physics",
            "typologies-2-typology_name": "Amatoric",
            "typologies-2-type_value": "Love, Passion, Friendship, Romance",
            "typologies-3-typology_name": "Socionics",
            "typologies-3-type_value": "Intuitive, Ethical, Extratim"
        }, follow_redirects=True)
        assert response.status_code == 200
        
        # Перевіряємо, що на цій сторінці логін
        # Використовуємо текст з шаблону login.html для більш надійної перевірки
        assert b"Log In" in response.data or b"Login" in response.data
        assert b"Email" in response.data
        assert b"Need an account?" in response.data

        new_user = User.query.filter_by(username=username).first()
        assert new_user is not None

def test_register_post_invalid(client, app):
    with app.app_context():
        response = client.post("/register", data={
            "username": unique_username("testuser2"),
            "email": unique_email("testuser"),
            "password": "newpassword",
            "confirm_password": "newpassword"
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b"Registration failed" in response.data

def test_user_profile_logged_in(client, app):
    with app.app_context():
        # Create the user before trying to log in
        username = unique_username("someuser")
        email = unique_email("someuser")
        user = User(username=username, email=email)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()

        # Now log in with the newly created user
        client.post("/login", data={
            "email": email,
            "password": "testpassword"
        }, follow_redirects=True)

        # Check the profile page
        response = client.get(f"/user/{username}")
        assert response.status_code == 200
        assert email.encode() in response.data  # Check the user's actual email

        # Використовуємо гарантовано унікальний email для оновлення
        unique_id = uuid.uuid4().hex[:8]
        updated_email = f"updated_{unique_id}@example.com"
        
        response = client.post(f"/user/{username}", data={
            "email": updated_email,
            "typology_name": "Temporistics",
            "type_value": "Past, Current, Future, Eternity"
        }, follow_redirects=True)
        assert response.status_code == 200

        updated_user = User.query.filter_by(username=username).first()
        assert updated_user.email == updated_email  # Перевіряємо, що email оновився до очікуваного значення


def test_user_profile_other_user(client, app):
    with app.app_context():
        # Create a user first
        username = unique_username("someuser")
        email = unique_email("someuser")
        user = User(username=username, email=email)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()

        # Now log in with the newly created user
        client.post("/login", data={
            "email": email,
            "password": "testpassword"
        }, follow_redirects=True)

        # Attempting to access a non-existent user's profile should now produce a 404
        response = client.get("/user/nonexistentuser")
        assert response.status_code == 404


def test_upload_profile_image(client, app):
    with app.app_context():
        # Создаем пользователя
        username = unique_username("imageuser")
        email = unique_email("imageuser")
        user = User(username=username, email=email)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()

    # Логинимся
    client.post("/login", data={
        "email": email,
        "password": "testpassword"
    }, follow_redirects=True)

    # Создаем фейковый файл изображение
    data = {
        "username": username,
        "email": email,
        "typology_name": "Temporistics",
        "type_value": "Past, Current, Future, Eternity",
        "latitude": "40.0",
        "longitude": "-73.0",
        "profile_image": (BytesIO(b"fake image content"), "test.png")
    }

    response = client.post("/edit_profile", data=data, content_type='multipart/form-data', follow_redirects=True)

    assert response.status_code == 200
    # Проверяем, что запись в БД обновилась
    with app.app_context():
        updated_user = User.query.filter_by(username=username).first()
        assert updated_user is not None
        assert updated_user.profile_image == "test.png"


def test_upload_invalid_image_format(client, app):
    with app.app_context():
        # Создаем пользователя
        username = unique_username("invalidimage")
        email = unique_email("invalidimage")
        user = User(username=username, email=email)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()

    # Логинимся
    client.post("/login", data={
        "email": email,
        "password": "testpassword"
    }, follow_redirects=True)

    # Пытаемся загрузить файл с неподходящим расширением
    data = {
        "username": username,
        "email": email,
        "typology_name": "Temporistics",
        "type_value": "Past, Current, Future, Eternity",
        "latitude": "40.0",
        "longitude": "-73.0",
        "profile_image": (BytesIO(b"fake image content"), "test.txt")  # неверный формат
    }

    response = client.post("/edit_profile", data=data, content_type='multipart/form-data', follow_redirects=True)
    # Ожидаем, что профиль не обновится, и увидим сообщение об ошибке
    assert response.status_code == 200
    
    # Перевіряємо, що форма все ще відображається (не виконане перенаправлення на профіль)
    assert b"Edit Profile" in response.data
    assert b"Save Changes" in response.data

    with app.app_context():
        updated_user = User.query.filter_by(username=username).first()
        # Проверяем, что картинка не установилась
        assert updated_user.profile_image is None


def test_edit_profile_another_user(client, app):
    # Проверяем сценарий попытки редактирования профиля другого пользователя
    with app.app_context():
        username1 = unique_username("user1")
        email1 = unique_email("user1")
        user1 = User(username=username1, email=email1)
        user1.set_password("password1")
        db.session.add(user1)
        db.session.commit()

        username2 = unique_username("user2")
        email2 = unique_email("user2")
        user2 = User(username=username2, email=email2)
        user2.set_password("password2")
        db.session.add(user2)
        db.session.commit()

    # Логинимся под user1
    client.post("/login", data={"email": email1, "password": "password1"}, follow_redirects=True)

    # Пытаемся редактировать профиль user2
    data = {
        "username": "hacker",
        "email": "hacker@example.com",
        "typology_name": "Temporistics",
        "type_value": "Past, Current, Future, Eternity",
        "latitude": "50.0",
        "longitude": "50.0"
    }
    response = client.post(f"/user/{username2}", data=data, follow_redirects=True)
    # Ожидаем ошибку или перенаправление на домашнюю страницу
    assert response.status_code == 200
    # Проверяем, что сообщение о недоступности профиля присутствует
    assert b"You do not have permission to view or edit this profile." in response.data

    with app.app_context():
        # Проверяем, что пользователь user2 не изменился
        updated_user2 = User.query.filter_by(username=username2).first()
        assert updated_user2.username == username2
        assert updated_user2.email == email2


def test_full_integration_cycle(client, app):
    # Полный цикл: регистрация → логин → изменение профиля → logout
    # 1. Регистрация
    username = unique_username("fullcycle")
    email = unique_email("fullcycle")
    register_data = {
        "username": username,
        "email": email,
        "password": "integrationpass",
        "confirm_password": "integrationpass",
        "typologies-0-typology_name": "Temporistics",
        "typologies-0-type_value": "Past, Current, Future, Eternity",
        "typologies-1-typology_name": "Psychosophia",
        "typologies-1-type_value": "Emotion, Logic, Will, Physics",
        "typologies-2-typology_name": "Amatoric",
        "typologies-2-type_value": "Love, Passion, Friendship, Romance",
        "typologies-3-typology_name": "Socionics",
        "typologies-3-type_value": "Intuitive, Ethical, Extratim"
    }
    response = client.post("/register", data=register_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your account has been created! You can now log in." in response.data

    # 2. Логин
    login_data = {
        "email": email,
        "password": "integrationpass"
    }
    response = client.post("/login", data=login_data, follow_redirects=True)
    assert response.status_code == 200
    
    # Перевіряємо, що користувач залогінився (перевіряємо наявність елементів, які є на сторінці після логіну)
    assert b"Logout" in response.data
    assert username.encode() in response.data
    
    # Перевіряємо авторизацію через запит до профілю
    response = client.get(f"/user/{username}")
    assert response.status_code == 200  # Доступ до профілю означає успішну авторизацію

    # 3. Изменение профиля
    edit_data = {
        "username": username + "_updated",
        "email": email,
        "typology_name": "Temporistics",
        "type_value": "Past, Current, Future, Eternity",
        "latitude": "45.0",
        "longitude": "-45.0"
    }
    response = client.post("/edit_profile", data=edit_data, follow_redirects=True)
    assert b"Profile updated successfully." in response.data

    with app.app_context():
        updated_user = User.query.filter_by(username=username + "_updated").first()
        assert updated_user is not None
        assert updated_user.latitude == 45.0
        assert updated_user.longitude == -45.0

    # 4. Logout
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    
    # Перевіряємо, що користувач розлогінився (перевіряємо наявність форми логіну)
    assert b"Login" in response.data
    assert b"Password" in response.data
    
    # Також перевіряємо, що доступ до профілю більше недоступний
    response = client.get(f"/user/{username}_updated")
    assert response.status_code == 302  # Має перенаправити на логін


def test_missing_geo_data_in_distance_calculation(client, app):
    # Проверяем поведение при отсутствующих данных геолокации
    with app.app_context():
        username1 = unique_username("geo1")
        email1 = unique_email("geo1")
        user1 = User(username=username1, email=email1, latitude=40.0, longitude=-73.0)
        user1.set_password("password1")
        db.session.add(user1)
        db.session.commit()

        username2 = unique_username("geo2")
        email2 = unique_email("geo2")
        # У второго пользователя отсутствуют координаты
        user2 = User(username=username2, email=email2)
        user2.set_password("password2")
        db.session.add(user2)
        db.session.commit()

    # Логинимся под user1
    client.post("/login", data={"email": email1, "password": "password1"}, follow_redirects=True)

    # Пытаемся открыть страницу nearby_compatibles или check_distance
    # На nearby_compatibles будут вычисляться расстояния, возможна ошибка
    response = client.get("/nearby_compatibles", follow_redirects=True)
    # Ожидаем, что раз пользователь без координат не вызовет краша, мы либо не увидим его в списке
    # либо будет какое-то предупреждение (в реальном коде можно добавить обработку таких случаев)
    assert response.status_code == 200
    # Проверяем, что не падаем с ошибкой 500
    # Можно добавить проверку на текст, если в коде есть flash об отсутствии координат,
    # но если нет — просто убедимся, что не 500.


def test_incorrect_geo_data_in_distance_calculation(client, app):
    # Если попытаться вычислить дистанцию при некорректных данных (например, нечисловых)
    with app.app_context():
        username1 = unique_username("geo3")
        email1 = unique_email("geo3")
        user1 = User(username=username1, email=email1, latitude=40.0, longitude=-73.0)
        user1.set_password("password3")
        db.session.add(user1)
        db.session.commit()

        username2 = unique_username("geo4")
        email2 = unique_email("geo4")
        # Попытаемся записать некорректные координаты (например, строку)
        user2 = User(username=username2, email=email2, latitude="not_a_number", longitude="-74.0")
        user2.set_password("password4")
        db.session.add(user2)
        # В реальности БД может упасть с ошибкой при commit, если нет проверок типов.
        # Предположим, что у нас float поля — тогда будет ошибка на уровне БД.
        # Если модель не защищена от такого ввода, этот тест покажет падение.
        # Для простоты считаем, что координаты валидируются где-то и просто None записывается при ошибке.
        db.session.commit()

    client.post("/login", data={"email": email1, "password": "password3"}, follow_redirects=True)
    response = client.get("/nearby_compatibles", follow_redirects=True)
    # Здесь мы просто убеждаемся, что код не падает.
    assert response.status_code == 200
    # Аналогично предыдущему тесту, если надо, можно добавить логику проверки flash сообщений или отсутствия пользователя в списке.
