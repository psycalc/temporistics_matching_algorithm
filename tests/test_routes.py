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

        # Чтобы избежать ошибки уникальности при обновлении username, сгенерируем новый username
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
        # Проверим, что обновление прошло успешно
        assert b"Profile updated successfully." in response.data
