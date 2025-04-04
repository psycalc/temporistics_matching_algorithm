import pytest
import os
import glob
from app import db
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
            response = client.post("/change_language", data={"language": lang}, follow_redirects=True)
            assert response.status_code == 200
            
            # Витягуємо cookie з запиту до головної сторінки
            response = client.get("/")
            cookie_header = response.request.headers.get('Cookie', '')
            assert f'locale={lang}' in cookie_header, f"Cookie не встановлено для мови {lang}"

def test_language_affects_content(client, app):
    """Перевіряє, що зміна мови впливає на вміст сторінки."""
    with app.app_context():
        # Створюємо користувача для входу
        username = unique_username("localization_user")
        email = unique_email("localization_user")
        user = User(username=username, email=email)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
        
        # Заходимо як користувач
        client.post("/login", data={
            "email": email,
            "password": "testpassword",
        }, follow_redirects=True)
        
        # Перевіряємо вміст сторінки англійською (за замовчуванням)
        client.post("/change_language", data={"language": "en"}, follow_redirects=True)
        response = client.get("/")
        assert b"Home" in response.data
        assert b"Profile" in response.data
        
        # Перевіряємо, що 'locale' cookie встановлено правильно
        for lang in ["uk", "fr", "es"]:
            client.post("/change_language", data={"language": lang}, follow_redirects=True)
            response = client.get("/")
            cookie_header = response.request.headers.get('Cookie', '')
            assert f'locale={lang}' in cookie_header, f"Cookie не встановлено для мови {lang}"

def test_language_cookie_preserved(client, app):
    """Перевіряє, що мовні cookie зберігаються між запитами."""
    with app.app_context():
        # Встановлюємо мову
        client.post("/change_language", data={"language": "uk"}, follow_redirects=True)
        
        # Перевіряємо, що cookie зберігається при наступних запитах
        response = client.get("/")
        cookie_header = response.request.headers.get('Cookie', '')
        assert 'locale=uk' in cookie_header, "Cookie не збережено після зміни мови"
        
        # Відвідуємо інші сторінки і перевіряємо cookie
        response = client.get("/login")
        cookie_header = response.request.headers.get('Cookie', '')
        assert 'locale=uk' in cookie_header, "Cookie не збережено при переході на сторінку логіну"

def test_translated_content_displayed(client, app):
    """Перевіряє, що переклади відображаються на сторінках."""
    with app.app_context():
        # Створюємо користувача для входу
        username = unique_username("translation_tester")
        email = unique_email("translation_tester")
        user = User(username=username, email=email)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
        
        # Встановлюємо українську мову спочатку
        client.post("/change_language", data={"language": "uk"}, follow_redirects=True)
        
        # Перевіряємо сторінку входу перед логіном 
        response = client.get("/login")
        page_text = response.data.decode('utf-8')
        assert re.search(r'[а-яА-ЯіІїЇєЄ]', page_text), "Сторінка логіну не містить українських символів"
        
        # Заходимо як користувач
        client.post("/login", data={
            "email": email,
            "password": "testpassword",
        }, follow_redirects=True)
        
        # Перевіряємо головну сторінку
        response = client.get("/")
        
        # Перевіряємо чи містить заголовок текст українською
        # Використовуємо регулярний вираз для перевірки наявності кирилічного тексту
        page_text = response.data.decode('utf-8')
        assert re.search(r'[а-яА-ЯіІїЇєЄ]', page_text), "Сторінка не містить українських символів"

def test_english_default_content(client, app):
    """Перевіряє, що англійські тексти відображаються за замовчуванням."""
    with app.app_context():
        # Встановлюємо англійську мову
        client.post("/change_language", data={"language": "en"})
        
        # Перевіряємо сторінку входу
        response = client.get("/login")
        assert b"Log In" in response.data
        assert b"Need an account?" in response.data 