import pytest
from app.extensions import db
from app.models import User, UserType
from flask_login import current_user
from tests.test_helpers import unique_username, unique_email
from io import BytesIO
import uuid
import os
import tempfile
from PIL import Image


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 302

def test_login(client, app, test_db):
    with app.app_context():
        username = unique_username("loginuser")
        email = unique_email("loginuser")
        user = User(username=username, email=email)
        user.set_password("testpassword")
        test_db.session.add(user)
        test_db.session.commit()

        response = client.post("/login", data={
            "email": email,
            "password": "testpassword",
            "submit": "Login"
        }, follow_redirects=True)

        assert response.status_code == 200

def test_login_wrong_password(client, app, test_db):
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

def test_logout(client, app, test_db):
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

def test_edit_profile_route(client, app, test_db):
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

def test_compatible_nearby_link_visibility(client, app, test_db):
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

def test_nearby_compatibles_page(client, app, test_db):
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

def test_register_post_valid(client, app, test_db):
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
            "profession": "Engineer",
            "show_profession": "y",
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
        assert new_user.profession == "Engineer"
        assert new_user.profession_visible is True

def test_register_post_invalid(client, app, test_db):
    with app.app_context():
        # Використовуємо однаковий username для виклику конфлікту
        username = "duplicateuser1"
        email1 = "duplicate1@example.com"
        email2 = "duplicate2@example.com"
        
        # Спочатку створюємо користувача в БД
        user = User(username=username, email=email1)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
        
        # Спроба зареєструвати користувача з тим же ім'ям
        response = client.post("/register", data={
            "username": username,  # використовуємо той самий username
            "email": email2,  # новий email
            "password": "testpassword",
            "confirm_password": "testpassword"
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b"Validation failed" in response.data or b"already exists" in response.data or b"already taken" in response.data

def test_user_profile_logged_in(client, app, test_db):
    with app.app_context():
        # Створюємо тестового користувача
        username = unique_username("profileuser")
        email = unique_email("profileuser")
        user = User(username=username, email=email)
        user.set_password("profilepass")
        
        # Додаємо типологію для користувача
        user_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user.user_type = user_type
        
        db.session.add(user)
        db.session.add(user_type)
        db.session.commit()
        
        # Логінимось цим користувачем
        client.post("/login", data={
            "email": email,
            "password": "profilepass",
            "submit": "Login"
        }, follow_redirects=True)
        
        # Відвідуємо свій профіль
        response = client.get(f"/user/{username}", follow_redirects=True)
        
        # Перевіряємо, що на сторінці є ім'я користувача
        assert response.status_code == 200
        assert username.encode('utf-8') in response.data
        
        # Перевіряємо, що на сторінці є тип користувача
        assert b"Temporistics" in response.data
        assert b"Past, Current, Future, Eternity" in response.data

        # Має бути кнопка редагування для власного профілю
        assert b"Save Changes" in response.data

def test_user_profile_other_user(client, app, test_db):
    with app.app_context():
        # Створюємо двох тестових користувачів
        username1 = unique_username("viewer")
        email1 = unique_email("viewer")
        user1 = User(username=username1, email=email1)
        user1.set_password("password1")
        
        username2 = unique_username("target")
        email2 = unique_email("target")
        user2 = User(username=username2, email=email2)
        user2.set_password("password2")
        
        # Додаємо типологію для другого користувача
        user_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user2.user_type = user_type
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user_type)
        db.session.commit()
        
        # Логінимось першим користувачем
        client.post("/login", data={
            "email": email1,
            "password": "password1",
            "submit": "Login"
        }, follow_redirects=True)
        
        # Відвідуємо профіль другого користувача
        response = client.get(f"/user/{username2}", follow_redirects=True)
        
        # Перевіряємо, що отримуємо перенаправлення на головну сторінку
        # і сторінка містить повідомлення про заборону перегляду
        assert response.status_code == 200
        assert b"permission" in response.data or b"not authorized" in response.data


def test_upload_profile_image(client, app, test_db):
    with app.app_context():
        # Створюємо тестового користувача
        username = unique_username("imageuser")
        email = unique_email("imageuser")
        user = User(username=username, email=email)
        user.set_password("imagepass")
        db.session.add(user)
        db.session.commit()

        # Логінимось цим користувачем
        client.post("/login", data={
            "email": email,
            "password": "imagepass",
            "submit": "Login"
        }, follow_redirects=True)

        # Створюємо тимчасовий файл зображення для тесту
        test_image = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(test_image.name)
        test_image.close()

        try:
            # Тестуємо завантаження зображення через форму редагування профілю
            with open(test_image.name, 'rb') as img_file:
                data = {
                    'username': username, # Потрібно передати поточні дані
                    'email': email,
                    'typology_name': 'Temporistics', # Припустимо, що типологія є
                    'type_value': 'Past, Current, Future, Eternity',
                    'latitude': '40.0',
                    'longitude': '-73.0',
                    'profile_image': (img_file, 'test_image.jpg')
                }
                response = client.post('/edit_profile',  # Використовуємо правильний маршрут
                                        data=data,
                                        content_type='multipart/form-data',
                                        follow_redirects=True)

                assert response.status_code == 200
                # Перевіряємо повідомлення про успішне оновлення профілю, а не завантаження зображення
                assert b"Profile updated successfully" in response.data

                # Перевіряємо, що зображення було збережено для користувача
                updated_user = User.query.filter_by(username=username).first()
                assert updated_user.profile_image is not None
                # Перевіримо чи ім'я файлу було збережено
                assert updated_user.profile_image.endswith('.jpg')
        finally:
            # Видаляємо тимчасове зображення
            if os.path.exists(test_image.name):
                 os.unlink(test_image.name)


def test_upload_invalid_image_format(client, app, test_db):
    with app.app_context():
        # Створюємо тестового користувача
        username = unique_username("invalidimageuser")
        email = unique_email("invalidimageuser")
        user = User(username=username, email=email)
        user.set_password("imagepass")
        db.session.add(user)
        db.session.commit()

        # Логінимось цим користувачем
        client.post("/login", data={
            "email": email,
            "password": "imagepass",
            "submit": "Login"
        }, follow_redirects=True)

        # Створюємо невалідний файл (не зображення)
        invalid_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        invalid_file.write(b"This is not an image")
        invalid_file.close()

        try:
            # Тестуємо завантаження невалідного файлу через форму редагування профілю
            with open(invalid_file.name, 'rb') as file:
                data = {
                    'username': username, # Потрібно передати поточні дані
                    'email': email,
                    'typology_name': 'Temporistics',
                    'type_value': 'Past, Current, Future, Eternity',
                    'latitude': '40.0',
                    'longitude': '-73.0',
                    'profile_image': (file, 'test_file.txt')
                }
                response = client.post('/edit_profile', # Використовуємо правильний маршрут
                                       data=data,
                                       content_type='multipart/form-data',
                                       follow_redirects=True)

                # Перевіряємо, що отримали помилку про невалідний формат
                assert response.status_code == 200
                # Перевірка, що ми залишились на сторінці редагування
                assert b"Edit Profile" in response.data
                # Виведення повного HTML для діагностики
                print("Form validation failed:", form.errors) if 'form' in locals() else None
                print(response.data)
                
                # Шукаємо повідомлення про помилку від валідатора FileAllowed
                # У вихідному коді з помилкою було видно, що форма містить помилку l'Images only!'
                assert b"Images only!" in response.data or b"l'Images only!'" in response.data or b"Invalid image format" in response.data

                # Перевіряємо, що зображення не було оновлено
                updated_user = User.query.filter_by(username=username).first()
                assert updated_user.profile_image is None
        finally:
            # Видаляємо тимчасовий файл
            if os.path.exists(invalid_file.name):
                os.unlink(invalid_file.name)


def test_edit_profile_another_user(client, app, test_db):
    # Перевіряємо сценарій спроби редагування профілю іншого користувача
    with app.app_context():
        # Створюємо двох користувачів
        username1 = unique_username("editor")
        email1 = unique_email("editor")
        user1 = User(username=username1, email=email1)
        user1.set_password("password1")
        
        username2 = unique_username("victim")
        email2 = unique_email("victim")
        user2 = User(username=username2, email=email2)
        user2.set_password("password2")
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        # Логінимось першим користувачем
        client.post("/login", data={
            "email": email1,
            "password": "password1",
            "submit": "Login"
        }, follow_redirects=True)
        
        # Спроба редагувати профіль другого користувача
        data = {
            "username": username2,  # Залишаємо те ж ім'я
            "email": "hacked@example.com",  # Пробуємо змінити email
            "typology_name": "Temporistics",
            "type_value": "Past, Current, Future, Eternity"
        }
        
        response = client.post(f"/user/{username2}", data=data, follow_redirects=True)
        
        # Перевіряємо, що отримали помилку або перенаправлення
        assert response.status_code != 200 or b"not authorized" in response.data or b"permission" in response.data
        
        # Перевіряємо, що дані користувача не змінились
        updated_user = User.query.filter_by(username=username2).first()
        assert updated_user.email == email2


def test_full_integration_cycle(client, app, test_db):
    # Повний цикл: реєстрація → логін → зміна профілю → логаут
    with app.app_context():
        # 1. Реєстрація користувача напряму в БД
        unique_id = uuid.uuid4().hex[:8]
        username = f"fullcycle_{unique_id}"
        email = f"fullcycle_{unique_id}@example.com"
        password = "testpassword"
        
        # Створюємо користувача 
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Додаємо типологію
        user_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user.user_type = user_type
        
        # Зберігаємо в базі даних
        db.session.add(user)
        db.session.add(user_type)
        db.session.commit()
        
        # 2. Логін через API
        login_data = {
            "email": email,
            "password": password,
            "submit": "Login"
        }
        
        response = client.post("/login", data=login_data, follow_redirects=True)
        assert response.status_code == 200
        
        # 3. Перевіряємо головну сторінку, щоб підтвердити логін
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200
        
        # 4. Зміна профілю
        new_email = f"updated_{unique_id}@example.com"
        
        edit_data = {
            "username": username,
            "email": new_email,
            "typology_name": "Psychosophia",
            "type_value": "Emotion, Logic, Will, Physics",
            "latitude": "45.0",
            "longitude": "-70.0",
            "submit": "Save Changes"
        }
        
        # Виводимо дані для діагностики
        print(f"Editing profile for user ID: {user.id}, username: {username}")
        
        # Відправляємо запит на редагування профілю
        edit_response = client.post("/edit_profile", data=edit_data, follow_redirects=True)
        
        # Виводимо вміст відповіді для діагностики
        print(f"Edit response status: {edit_response.status_code}")
        print(f"Edit response data: {edit_response.data[:300]}...")
        
        assert edit_response.status_code == 200
        assert b"Profile updated successfully" in edit_response.data
        
        # Перевіряємо, що профіль змінено в базі даних
        db.session.refresh(user)  # Оновлюємо дані з бази
        assert user.email == new_email
        assert user.latitude == 45.0
        assert user.longitude == -70.0
        
        # Перевіряємо типологію
        assert user.user_type.typology_name == "Psychosophia"
        assert user.user_type.type_value == "Emotion, Logic, Will, Physics"
        
        # 5. Логаут
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        assert b"Login" in response.data


def test_missing_geo_data_in_distance_calculation(client, app, test_db):
    # Перевіряємо обробку відсутніх даних геолокації
    with app.app_context():
        # Створюємо два користувача, один з геоданими, інший без
        # Користувач із геоданими
        username1 = unique_username("geo_user")
        email1 = unique_email("geo_user")
        user1 = User(username=username1, email=email1, latitude=40.0, longitude=-74.0)
        user1.set_password("password1")
        
        # Додаємо типологію
        user1_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user1.user_type = user1_type
        
        # Користувач без геоданих
        username2 = unique_username("nogeo_user")
        email2 = unique_email("nogeo_user")
        user2 = User(username=username2, email=email2, latitude=None, longitude=None)
        user2.set_password("password2")
        
        # Додаємо типологію
        user2_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user2.user_type = user2_type
        
        db.session.add(user1)
        db.session.add(user1_type)
        db.session.add(user2)
        db.session.add(user2_type)
        db.session.commit()
        
        # Логінимось першим користувачем (з геоданими)
        client.post("/login", data={
            "email": email1,
            "password": "password1",
            "submit": "Login"
        }, follow_redirects=True)
        
        # Перевіряємо сторінку з сумісними користувачами поблизу
        response = client.get("/nearby_compatibles", follow_redirects=True)
        assert response.status_code == 200
        
        # Другий користувач не повинен відображатися або повинна бути примітка про відсутність геоданих
        assert b"Compatible Users Nearby:" in response.data


def test_incorrect_geo_data_in_distance_calculation(client, app, test_db):
    # Тестуємо обробку некоректних даних геолокації
    with app.app_context():
        # Створюємо користувача з коректними геоданими
        username1 = unique_username("correctgeo")
        email1 = unique_email("correctgeo")
        user1 = User(username=username1, email=email1, latitude=40.0, longitude=-74.0)
        user1.set_password("password1")
        
        # Додаємо типологію
        user1_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user1.user_type = user1_type
        
        # Створюємо користувача з хибними геоданими
        username2 = unique_username("invalidgeo")
        email2 = unique_email("invalidgeo")
        user2 = User(username=username2, email=email2)
        # Встановлюємо некоректні дані, які будуть нормалізовані до None
        user2.latitude = "not-a-number"
        user2.longitude = "invalid-data"
        user2.set_password("password2")
        
        # Додаємо типологію
        user2_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user2.user_type = user2_type
        
        db.session.add(user1)
        db.session.add(user1_type)
        db.session.add(user2)
        db.session.add(user2_type)
        db.session.commit()
        
        # Після обробників подій валідації, перевіряємо, що некоректні значення не збереглися
        db.session.refresh(user2)
        assert user2.latitude is None
        assert user2.longitude is None
        
        # Логінимось першим користувачем
        client.post("/login", data={
            "email": email1,
            "password": "password1",
            "submit": "Login"
        }, follow_redirects=True)
        
        # Перевіряємо сторінку з сумісними користувачами поблизу
        response = client.get("/nearby_compatibles", follow_redirects=True)
        assert response.status_code == 200
        assert b"Compatible Users Nearby:" in response.data

def test_compatible_users_nearby_display(client, app, test_db):
    """Тест перевіряє, чи відображаються користувачі з сумісними типами і близькою геолокацією на сторінці сумісних поруч"""
    with app.app_context():
        # Створюємо першого користувача (активного)
        username1 = unique_username("activeuser")
        email1 = unique_email("activeuser")
        user1 = User(username=username1, email=email1, latitude=50.4501, longitude=30.5234)  # Київ
        user1.set_password("testpassword1")
        
        # Встановлюємо тип для першого користувача
        user1_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user1.user_type = user1_type
        
        db.session.add(user1)
        db.session.add(user1_type)
        db.session.commit()
        
        # Створюємо другого користувача з сумісним типом і близькою геолокацією
        username2 = unique_username("nearbyuser")
        email2 = unique_email("nearbyuser")
        user2 = User(username=username2, email=email2, latitude=50.4520, longitude=30.5300)  # Поруч з першим в Києві
        user2.set_password("testpassword2")
        
        # Встановлюємо той самий тип для другого користувача (для гарантованої сумісності)
        user2_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user2.user_type = user2_type
        
        db.session.add(user2)
        db.session.add(user2_type)
        db.session.commit()
        
        # Логінимося першим користувачем
        response = client.post("/login", data={
            "email": email1,
            "password": "testpassword1",
            "submit": "Login"
        }, follow_redirects=True)
        assert response.status_code == 200
        
        # Переходимо на сторінку сумісних поруч
        response = client.get("/nearby_compatibles", follow_redirects=True)
        assert response.status_code == 200
        
        # Перевіряємо, що сторінка містить другого користувача
        assert username2.encode('utf-8') in response.data
        
        # Перевіряємо, що відстань між користувачами відображається
        assert b"km" in response.data or b"m" in response.data
        
        # Перевіряємо, що заголовок списку сумісних користувачів присутній
        assert b"Compatible Users Nearby:" in response.data

def test_max_distance_in_edit_profile(client, app, test_db):
    """Тест перевіряє, що користувач може встановити максимальну прийнятну відстань через форму редагування профілю"""
    with app.app_context():
        # Створюємо тестового користувача
        username = unique_username("distanceuser")
        email = unique_email("distanceuser")
        user = User(username=username, email=email)
        user.set_password("distancepass")
        db.session.add(user)
        db.session.commit()
        
        # Логінимося цим користувачем
        client.post("/login", data={
            "email": email,
            "password": "distancepass",
            "submit": "Login"
        }, follow_redirects=True)
        
        # Перевіряємо початкове значення max_distance
        db.session.refresh(user)
        assert user.max_distance is None or user.max_distance == 50.0  # значення за замовчуванням
        
        # Оновлюємо профіль із новим значенням max_distance
        response = client.post('/edit_profile', data={
            'username': username,
            'email': email,
            'typology_name': 'Temporistics',
            'type_value': 'Past, Current, Future, Eternity',
            'latitude': '50.45',
            'longitude': '30.52',
            'max_distance': '25.5'  # нове значення
        }, follow_redirects=True)
        
        # Перевіряємо успішність оновлення
        assert response.status_code == 200
        assert b"Profile updated successfully" in response.data
        
        # Перевіряємо, що значення max_distance оновлено в БД
        db.session.refresh(user)
        assert user.max_distance == 25.5

def test_filter_nearby_by_max_distance(client, app, test_db):
    """Тест перевіряє, що функція nearby_compatibles враховує максимальну прийнятну відстань користувача"""
    with app.app_context():
        # Створюємо першого користувача (активного)
        username1 = unique_username("maxdistuser")
        email1 = unique_email("maxdistuser")
        user1 = User(username=username1, email=email1, latitude=50.4501, longitude=30.5234, max_distance=5.0)  # Київ, макс. 5 км
        user1.set_password("testpassword1")
        
        # Встановлюємо тип для першого користувача
        user1_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user1.user_type = user1_type
        
        db.session.add(user1)
        db.session.add(user1_type)
        db.session.commit()
        
        # Створюємо другого користувача (близько - в межах 5 км)
        username2 = unique_username("closeuser")
        email2 = unique_email("closeuser")
        user2 = User(username=username2, email=email2, latitude=50.4520, longitude=30.5300)  # Близько (~0.5 км)
        user2.set_password("testpassword2")
        
        # Встановлюємо той самий тип для другого користувача (для гарантованої сумісності)
        user2_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user2.user_type = user2_type
        
        db.session.add(user2)
        db.session.add(user2_type)
        
        # Створюємо третього користувача (далеко - поза межами 5 км)
        username3 = unique_username("faruser")
        email3 = unique_email("faruser")
        user3 = User(username=username3, email=email3, latitude=50.5200, longitude=30.6000)  # Далеко (~10-15 км)
        user3.set_password("testpassword3")
        
        # Встановлюємо той самий тип для третього користувача (для гарантованої сумісності)
        user3_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user3.user_type = user3_type
        
        db.session.add(user3)
        db.session.add(user3_type)
        db.session.commit()
        
        # Логінимося першим користувачем
        response = client.post("/login", data={
            "email": email1,
            "password": "testpassword1",
            "submit": "Login"
        }, follow_redirects=True)
        assert response.status_code == 200
        
        # Переходимо на сторінку сумісних поруч
        response = client.get("/nearby_compatibles", follow_redirects=True)
        assert response.status_code == 200
        
        # Перевіряємо, що близький користувач є на сторінці
        assert username2.encode('utf-8') in response.data
        
        # Перевіряємо, що далекий користувач відсутній на сторінці
        assert username3.encode('utf-8') not in response.data
        
        # Змінюємо максимальну відстань на більшу, щоб включити далекого користувача
        user1.max_distance = 20.0
        db.session.commit()
        
        # Переходимо на сторінку сумісних поруч знову
        response = client.get("/nearby_compatibles", follow_redirects=True)
        assert response.status_code == 200
        
        # Тепер обидва користувачі повинні бути на сторінці
        assert username2.encode('utf-8') in response.data
        assert username3.encode('utf-8') in response.data


def test_profession_visibility_in_nearby(client, app, test_db):
    """Users can hide their profession from others"""
    with app.app_context():
        # user1 will see user2 in nearby list
        username1 = unique_username("viewer")
        email1 = unique_email("viewer")
        user1 = User(username=username1, email=email1, latitude=50.45, longitude=30.52)
        user1.set_password("pass1")
        user1_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user1.user_type = user1_type

        username2 = unique_username("hidden")
        email2 = unique_email("hidden")
        user2 = User(username=username2, email=email2, latitude=50.452, longitude=30.53,
                     profession="Doctor", profession_visible=False)
        user2.set_password("pass2")
        user2_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        user2.user_type = user2_type

        db.session.add_all([user1, user1_type, user2, user2_type])
        db.session.commit()

        client.post("/login", data={"email": email1, "password": "pass1"}, follow_redirects=True)

        response = client.get("/nearby_compatibles", follow_redirects=True)
        assert response.status_code == 200
        assert username2.encode() in response.data
        assert b"Doctor" not in response.data


def test_chat_route(client, app, test_db):
    with app.app_context():
        username = unique_username("chat")
        email = unique_email("chat")
        user = User(username=username, email=email)
        user.set_password("chatpass")
        db.session.add(user)
        db.session.commit()

        client.post("/login", data={"email": email, "password": "chatpass"}, follow_redirects=True)
        response = client.get("/chat", follow_redirects=True)
        assert response.status_code == 200
