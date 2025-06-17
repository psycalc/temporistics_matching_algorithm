import pytest
from haversine import haversine
from app.services import get_users_distance, get_typology_instance
from app.models import User, UserType
from app.extensions import db

def test_haversine_distance():
    """Тестує функцію ``haversine`` з бібліотеки, яка обчислює відстань між двома точками на Землі."""
    # Координати Києва
    kyiv_lat, kyiv_lon = 50.4501, 30.5234
    
    # Координати Львова
    lviv_lat, lviv_lon = 49.8397, 24.0297
    
    # Очікувана відстань між Києвом та Львовом (приблизно 470 км)
    expected_distance = 470
    
    # Обчислюємо відстань за допомогою бібліотеки
    distance = haversine((kyiv_lat, kyiv_lon), (lviv_lat, lviv_lon))
    
    # Перевіряємо, що відстань приблизно відповідає очікуваній (з похибкою 10 км)
    assert abs(distance - expected_distance) <= 10, f"Розрахована відстань {distance} занадто відрізняється від очікуваної {expected_distance}"

def test_haversine_distance_same_point():
    """Тестує ``haversine`` для випадку однакових координат."""
    # Координати точки
    lat, lon = 50.4501, 30.5234
    
    # Відстань між точкою та нею самою повинна бути 0
    distance = haversine((lat, lon), (lat, lon))
    
    # Перевіряємо, що відстань дорівнює 0
    assert distance == 0, f"Відстань між однаковими точками повинна бути 0, але отримано {distance}"

def test_haversine_distance_antipodes():
    """Тестує ``haversine`` для антиподів (протилежних точок на Землі)."""
    # Координати точки та її антипода (приблизно)
    lat1, lon1 = 50.0, 30.0
    lat2, lon2 = -50.0, -150.0  # Протилежна точка
    
    # Приблизна максимальна відстань на Землі (половина довжини екватора)
    earth_circumference = 40075  # км
    expected_distance = earth_circumference / 2
    
    # Обчислюємо відстань за допомогою бібліотеки
    distance = haversine((lat1, lon1), (lat2, lon2))
    
    # Перевіряємо, що відстань приблизно відповідає половині довжини екватора
    assert abs(distance - expected_distance) <= 100, f"Розрахована відстань {distance} занадто відрізняється від очікуваної {expected_distance}"

def test_haversine_distance_equator():
    """Тестує ``haversine`` для точок на екваторі."""
    # Координати двох точок на екваторі, розділених 90 градусами довготи
    lat1, lon1 = 0.0, 0.0
    lat2, lon2 = 0.0, 90.0
    
    # Приблизна очікувана відстань (чверть довжини екватора)
    earth_circumference = 40075  # км
    expected_distance = earth_circumference / 4
    
    # Обчислюємо відстань за допомогою бібліотеки
    distance = haversine((lat1, lon1), (lat2, lon2))
    
    # Перевіряємо, що відстань приблизно відповідає чверті довжини екватора
    assert abs(distance - expected_distance) <= 50, f"Розрахована відстань {distance} занадто відрізняється від очікуваної {expected_distance}"

def test_get_users_distance(app, test_db):
    """Тестує функцію get_users_distance, яка обчислює відстань між двома користувачами."""
    with app.app_context():
        # Створюємо двох користувачів з координатами
        user1 = User(username="testuser1", email="test1@example.com",
                    latitude=50.4501, longitude=30.5234)  # Київ
        user2 = User(username="testuser2", email="test2@example.com",
                    latitude=49.8397, longitude=24.0297)  # Львів
        
        db.session.add_all([user1, user2])
        db.session.commit()
        
        # Очікувана відстань між Києвом та Львовом (приблизно 470 км)
        expected_distance = 470
        
        # Обчислюємо відстань за допомогою функції
        distance = get_users_distance(user1, user2)
        
        # Перевіряємо, що відстань приблизно відповідає очікуваній (з похибкою 10 км)
        assert abs(distance - expected_distance) <= 10, f"Розрахована відстань {distance} занадто відрізняється від очікуваної {expected_distance}"

def test_get_users_distance_missing_coordinates(app, test_db):
    """Тестує функцію get_users_distance у випадку відсутності координат у користувачів."""
    with app.app_context():
        # Створюємо двох користувачів без координат
        user1 = User(username="testuser3", email="test3@example.com")
        user2 = User(username="testuser4", email="test4@example.com",
                    latitude=49.8397, longitude=24.0297)  # Тільки другий користувач має координати
        
        db.session.add_all([user1, user2])
        db.session.commit()
        
        # Очікуємо виключення ValueError, оскільки у першого користувача відсутні координати
        with pytest.raises(ValueError, match="Both users must have coordinates set"):
            get_users_distance(user1, user2)

def test_get_typology_instance(app):
    """Тестує функцію get_typology_instance, яка повертає екземпляр класу типології."""
    with app.app_context():
        # Перевіряємо, що функція повертає правильні екземпляри класів для різних типологій
        # Temporistics
        typology = get_typology_instance("Temporistics")
        assert typology is not None
        assert typology.__class__.__name__ == "TypologyTemporistics"
        
        # Psychosophia
        typology = get_typology_instance("Psychosophia")
        assert typology is not None
        assert typology.__class__.__name__ == "TypologyPsychosophia"
        
        # Socionics
        typology = get_typology_instance("Socionics")
        assert typology is not None
        assert typology.__class__.__name__ == "TypologySocionics"
        
        # Неіснуюча типологія
        typology = get_typology_instance("NonExistentTypology")
        assert typology is None 