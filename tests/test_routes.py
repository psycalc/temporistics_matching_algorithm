import pytest
from app import db
from app.models import User, UserType
from flask_login import current_user
from tests.test_helpers import unique_username, unique_email
from io import BytesIO


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
            "typologies-3-type_value": "Intuitive, Ethical, Extratim"
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b"Your account has been created! You can now log in." in response.data

        new_user = User.query.filter_by(username="newuser").first()
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

        # Update the user's email
        response = client.post(f"/user/{username}", data={
            "email": "updated@example.com",
            "typology_name": "Temporistics",
            "type_value": "Past, Current, Future, Eternity"
        }, follow_redirects=True)
        assert response.status_code == 200

        updated_user = User.query.filter_by(username=username).first()
        assert updated_user.email == "updated@example.com"


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

