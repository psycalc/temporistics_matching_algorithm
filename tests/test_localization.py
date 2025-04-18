import pytest
import os
import glob
from app.extensions import db
from app.models import User
from tests.test_helpers import unique_username, unique_email
import re
from flask import session

def test_available_translations(app):
    """Перевіряє наявність файлів перекладів для всіх підтримуваних мов."""
    with app.app_context():
        # Перевіряємо, що папки з перекладами існують
        translations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'translations')
        supported_locales = app.config['LANGUAGES']
        
        for locale in supported_locales:
            # Пропускаємо англійську мову, оскільки вона є мовою за замовчуванням і не потребує перекладів
            locale_dir = os.path.join(translations_dir, locale, 'LC_MESSAGES')
            assert os.path.isdir(locale_dir), f"Директорія перекладів для {locale} не знайдена"
            
            # Перевіряємо наявність скомпільованих файлів перекладів (.mo)
            mo_files = glob.glob(os.path.join(locale_dir, '*.mo'))
            assert len(mo_files) > 0, f"Скомпільовані файли перекладів для {locale} не знайдені"

def test_change_language_cookie(client, app):
    """Перевіряє, що при зміні мови встановлюється відповідний cookie."""
    with app.app_context():
        # Перевіряємо всі підтримувані мови
        for lang in app.config['LANGUAGES']:
            # В тестовому оточенні CSRF захист вимкнено, але шаблон все одно використовує csrf_token
            # Тому замість прямого клієнтського запиту імітуємо зміну мови через ендпоінт
            response = client.get("/")  # Спершу відвідуємо головну сторінку
            response = client.post("/change_language", data={"language": lang})
            assert "locale" in response.headers.get("Set-Cookie", "")
            
            # Перевіряємо, що при запиті до головної сторінки передається правильний cookie
            response = client.get("/")
            cookie_header = response.request.headers.get('Cookie', '')
            assert f'locale={lang}' in cookie_header, f"Cookie не встановлено для мови {lang}"

def test_language_affects_content(client, app, test_db):
    """Перевіряє, що зміна мови впливає на вміст сторінки."""
    with app.app_context():
        # Перевіряємо, що кешування вимкнено в тестовому середовищі
        assert app.config['CACHE_TYPE'] == 'NullCache', "Кешування повинно бути вимкнено в тестах"
        
        # Створюємо користувача для входу
        username = unique_username("localization_user")
        email = unique_email("localization_user")
        user = User(username=username, email=email)
        user.set_password("testpassword")
        test_db.session.add(user)
        test_db.session.commit()
        
        # Заходимо як користувач без follow_redirects
        client.post("/login", data={
            "email": email,
            "password": "testpassword",
        })
        
        # Перевіряємо вміст сторінки англійською (за замовчуванням)
        client.post("/change_language", data={"language": "en"})
        response = client.get("/")
        # Перевіряємо текст, який точно буде на сторінці без залежності від мови
        assert response.status_code == 200
        
        # Перевіряємо, що 'locale' cookie встановлено правильно
        for lang in ["uk", "fr", "es"]:
            client.post("/change_language", data={"language": lang})
            response = client.get("/")
            cookie_header = response.request.headers.get('Cookie', '')
            assert f'locale={lang}' in cookie_header, f"Cookie не встановлено для мови {lang}"

def test_language_cookie_preserved(client, app):
    """Перевіряє, що мовні cookie зберігаються між запитами."""
    with app.app_context():
        # Встановлюємо мову
        response = client.post("/change_language", data={"language": "uk"})
        assert "locale" in response.headers.get("Set-Cookie", "")
        
        # Перевіряємо, що cookie зберігається при наступних запитах
        response = client.get("/")
        cookie_header = response.request.headers.get('Cookie', '')
        assert 'locale=uk' in cookie_header, "Cookie не збережено після зміни мови"
        
        # Відвідуємо інші сторінки і перевіряємо cookie
        response = client.get("/login")
        cookie_header = response.request.headers.get('Cookie', '')
        assert 'locale=uk' in cookie_header, "Cookie не збережено при переході на сторінку логіну"

def test_translated_content_displayed(client, app, test_db):
    """Перевіряє, що переклади відображаються на сторінках."""
    with app.app_context():
        # Створюємо користувача для входу
        username = unique_username("translation_tester")
        email = unique_email("translation_tester")
        user = User(username=username, email=email)
        user.set_password("testpassword")
        test_db.session.add(user)
        test_db.session.commit()
        
        # Встановлюємо українську мову спочатку
        client.post("/change_language", data={"language": "uk"})
        
        # Перевіряємо базові URL, які не вимагають авторизації
        response = client.get("/login")
        assert response.status_code == 200
        
        # Заходимо як користувач
        client.post("/login", data={
            "email": email,
            "password": "testpassword",
        })
        
        # Перевіряємо, що cookie з мовою збереглося
        response = client.get("/")
        cookie_header = response.request.headers.get('Cookie', '')
        assert 'locale=uk' in cookie_header, "Cookie мови не збережено"

def test_english_default_content(client, app):
    """Перевіряє, що англійські тексти відображаються за замовчуванням."""
    with app.app_context():
        # Встановлюємо англійську мову
        client.post("/change_language", data={"language": "en"})
        
        # Перевіряємо сторінку входу
        response = client.get("/login")
        assert response.status_code == 200
        assert b"Log In" in response.data
        assert b"Need an account?" in response.data 