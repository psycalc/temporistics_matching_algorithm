import logging
import io
import os
import time
import uuid

import pytest
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException

logger = logging.getLogger(__name__)

if not os.environ.get("RUN_SELENIUM"):
    pytest.skip("Skipping selenium tests; RUN_SELENIUM not set", allow_module_level=True)
from tests.test_helpers import unique_username, unique_email

@pytest.fixture(scope="function")
def driver():
    """Фікстура для створення і закриття драйвера браузера."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Новий формат headless для Chrome
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    chrome_options.binary_location = '/usr/bin/chromium-browser'
    try:
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except WebDriverException as e:
        logger.error("\u041f\u043e\u043c\u0438\u043b\u043a\u0430 \u043f\u0440\u0438 \u0456\u043d\u0456\u0446\u0456\u0430\u043b\u0456\u0437\u0430\u0446\u0456\u0457 Chrome: %s", e)
        raise

    logger.info("ChromeDriver \u0443\u0441\u043f\u0456\u0448\u043d\u043e \u0456\u043d\u0456\u0446\u0456\u0430\u043b\u0456\u0437\u043e\u0432\u0430\u043d\u043e")
    
    # Встановлюємо неявне очікування
    driver.implicitly_wait(10)
    
    yield driver
    
    # Закриваємо браузер після тесту
    logger.info("\u0417\u0430\u043a\u0440\u0438\u0432\u0430\u0454\u043c\u043e \u0434\u0440\u0430\u0439\u0432\u0435\u0440 \u043f\u0456\u0441\u043b\u044f \u0442\u0435\u0441\u0442\u0443")
    driver.quit()

def create_test_image():
    """Створює тестове зображення в форматі PNG."""
    file = io.BytesIO()
    image = Image.new('RGB', size=(100, 100), color=(255, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file

@pytest.mark.selenium
def test_user_registration(driver, app, live_server):
    """
    Тестує процес реєстрації нового користувача через веб-інтерфейс.
    
    Цей тест:
    1. Відкриває сторінку реєстрації
    2. Заповнює форму реєстрації
    3. Відправляє форму і перевіряє успішність реєстрації
    """
    live_server_url = live_server.url
    logger.debug("URL \u0442\u0435\u0441\u0442\u043e\u0432\u043e\u0433\u043e \u0441\u0435\u0440\u0432\u0435\u0440\u0430: %s", live_server_url)
    
    # Генеруємо унікальні дані для тесту
    test_username = unique_username("selenium_test")
    test_email = unique_email("selenium", "test.com")
    test_password = "TestPassword123!"
    
    # Відкриваємо сторінку реєстрації
    driver.get(f"{live_server_url}/register")
    
    try:
        # Заповнюємо форму реєстрації
        driver.find_element(By.ID, "username").send_keys(test_username)
        driver.find_element(By.ID, "email").send_keys(test_email)
        driver.find_element(By.ID, "password").send_keys(test_password)
        driver.find_element(By.ID, "confirm_password").send_keys(test_password)
        
        # Заповнюємо дані типології (якщо вони є у формі)
        typology_elements = driver.find_elements(By.CSS_SELECTOR, "select[name^='typologies']")
        if typology_elements:
            for select_element in typology_elements:
                # Вибираємо перший варіант для кожного селекту
                select = Select(select_element)
                options = select.options
                if len(options) > 0:
                    select.select_by_index(0)
        
        # Відправляємо форму
        driver.find_element(By.ID, "submit").click()
        
        # Перевіряємо, що потрапили на сторінку логіну
        WebDriverWait(driver, 10).until(
            EC.url_contains("/login")
        )
        
        # Перевіряємо, що є повідомлення про успішну реєстрацію
        flash_messages = driver.find_elements(By.CLASS_NAME, "alert-success")
        assert any("account has been created" in msg.text for msg in flash_messages), "Повідомлення про успішну реєстрацію не знайдено"
        
        logger.info("\u2713 \u0420\u0435\u0454\u0441\u0442\u0440\u0430\u0446\u0456\u044f \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0430 %s \u043f\u0440\u043e\u0439\u0448\u043b\u0430 \u0443\u0441\u043f\u0456\u0448\u043d\u043e", test_username)
        
    except Exception as e:
        logger.error("\u041f\u043e\u043c\u0438\u043b\u043a\u0430 \u043f\u0440\u0438 \u0440\u0435\u0454\u0441\u0442\u0440\u0430\u0446\u0456\u0457 \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0430: %s", e)
        # Знімок екрану для діагностики
        driver.save_screenshot("registration_error.png")
        raise

@pytest.mark.selenium
def test_user_login_logout(driver, app, live_server, test_db):
    """
    Тестує процес входу і виходу користувача.
    
    Цей тест:
    1. Створює тестового користувача в базі даних
    2. Відкриває сторінку входу і заповнює форму
    3. Перевіряє успішність входу
    4. Виконує вихід і перевіряє успішність виходу
    """
    with app.app_context():
        # Створюємо тестового користувача в базі даних
        from app.models import User
        from app.extensions import db
        
        test_username = unique_username("selenium_login")
        test_email = unique_email("selenium_login", "test.com")
        test_password = "TestPassword123!"
        
        user = User(username=test_username, email=test_email)
        user.set_password(test_password)
        db.session.add(user)
        db.session.commit()
    
    live_server_url = live_server.url
    
    try:
        # Відкриваємо сторінку входу
        driver.get(f"{live_server_url}/login")
        
        # Заповнюємо форму входу
        driver.find_element(By.ID, "email").send_keys(test_email)
        driver.find_element(By.ID, "password").send_keys(test_password)
        driver.find_element(By.ID, "submit").click()
        
        # Перевіряємо, що потрапили на головну сторінку
        WebDriverWait(driver, 10).until(
            EC.url_contains("/")
        )
        
        # Перевіряємо, що в меню є пункт "Logout" після входу
        logout_link = driver.find_element(By.XPATH, "//a[contains(@href, '/logout')]")
        assert logout_link.is_displayed(), "Посилання для виходу не знайдено після входу"
        
        logger.info("\u2713 \u0412\u0445\u0456\u0434 \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0430 %s \u043f\u0440\u043e\u0439\u0448\u043e\u0432 \u0443\u0441\u043f\u0456\u0448\u043d\u043e", test_username)
        
        # Тепер тестуємо вихід
        logout_link.click()
        
        # Перевіряємо, що перенаправлені на сторінку входу
        WebDriverWait(driver, 10).until(
            EC.url_contains("/login")
        )
        
        # Перевіряємо, що в меню є пункт "Login" після виходу
        login_link = driver.find_element(By.XPATH, "//a[contains(@href, '/login')]")
        assert login_link.is_displayed(), "Посилання для входу не знайдено після виходу"
        
        logger.info("\u2713 \u0412\u0438\u0445\u0456\u0434 \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0430 \u043f\u0440\u043e\u0439\u0448\u043e\u0432 \u0443\u0441\u043f\u0456\u0448\u043d\u043e")
        
    except Exception as e:
        logger.error("\u041f\u043e\u043c\u0438\u043b\u043a\u0430 \u043f\u0440\u0438 \u0442\u0435\u0441\u0442\u0443\u0432\u0430\u043d\u043d\u0456 \u0432\u0445\u043e\u0434\u0443/\u0432\u0438\u0445\u043e\u0434\u0443: %s", e)
        driver.save_screenshot("login_logout_error.png")
        raise

@pytest.mark.selenium
def test_edit_profile(driver, app, live_server, test_db):
    """
    Тестує редагування профілю користувача.
    
    Цей тест:
    1. Створює тестового користувача і виконує вхід
    2. Відкриває сторінку редагування профілю
    3. Заповнює форму новими даними
    4. Відправляє форму і перевіряє успішність редагування
    """
    with app.app_context():
        # Створюємо тестового користувача в базі даних
        from app.models import User, UserType
        from app.extensions import db
        
        test_username = unique_username("selenium_edit")
        test_email = unique_email("selenium_edit", "test.com")
        test_password = "TestPassword123!"
        
        user = User(username=test_username, email=test_email, 
                   latitude=50.4501, longitude=30.5234)  # Координати Києва
        user.set_password(test_password)
        
        # Створюємо тип користувача
        user_type = UserType(typology_name="Temporistics", 
                           type_value="Past, Current, Future, Eternity")
        db.session.add(user_type)
        db.session.flush()
        
        user.type_id = user_type.id
        db.session.add(user)
        db.session.commit()
    
    live_server_url = live_server.url
    
    try:
        # Відкриваємо сторінку входу і входимо
        driver.get(f"{live_server_url}/login")
        driver.find_element(By.ID, "email").send_keys(test_email)
        driver.find_element(By.ID, "password").send_keys(test_password)
        driver.find_element(By.ID, "submit").click()
        
        # Переходимо безпосередньо на сторінку редагування профілю
        driver.get(f"{live_server_url}/edit_profile")
        
        # Чекаємо завантаження сторінки редагування
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "latitude"))
        )
        
        # Змінюємо дані профілю
        new_lat = "51.5074"  # Координати Лондона
        new_lon = "-0.1278"
        new_max_distance = "100.0"
        
        # Генеруємо новий email для перевірки успішності зміни
        new_email = unique_email("updated_edit", "test.com")
        
        # Заповнюємо необхідні дані
        username_field = driver.find_element(By.ID, "username")
        username_field.clear()
        username_field.send_keys(test_username)
        
        email_field = driver.find_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys(new_email)
        
        typology_field = driver.find_element(By.ID, "typology_name")
        typology_field.clear()
        typology_field.send_keys("Temporistics")
        
        type_field = driver.find_element(By.ID, "type_value")
        type_field.clear()
        type_field.send_keys("Past, Current, Future, Eternity")
        
        lat_field = driver.find_element(By.ID, "latitude")
        lat_field.clear()
        lat_field.send_keys(new_lat)
        
        lon_field = driver.find_element(By.ID, "longitude")
        lon_field.clear()
        lon_field.send_keys(new_lon)
        
        max_distance_field = driver.find_element(By.ID, "max_distance")
        max_distance_field.clear()
        max_distance_field.send_keys(new_max_distance)
        
        # Відправляємо форму
        driver.find_element(By.ID, "submit").click()
        
        # Чекаємо, щоб сторінка завантажилась і перевіряємо перенаправлення
        time.sleep(2)  # Коротка пауза для впевненості що форма була оброблена
        
        # Перевіряємо, чи присутнє на сторінці успішне повідомлення
        assert "Profile updated successfully" in driver.page_source, "Повідомлення про успішне оновлення не відображається"
        
        # Перевіряємо, що ми на сторінці профілю (містить ім'я користувача)
        assert test_username in driver.page_source, "Ім'я користувача не знайдено на сторінці"
        
        logger.info("\u2713 \u0420\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u043d\u043d\u044f \u043f\u0440\u043e\u0444\u0456\u043b\u044e \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0430 %s \u043f\u0440\u043e\u0439\u0448\u043b\u043e \u0443\u0441\u043f\u0456\u0448\u043d\u043e", test_username)
        
    except Exception as e:
        logger.error("\u041f\u043e\u043c\u0438\u043b\u043a\u0430 \u043f\u0440\u0438 \u0440\u0435\u0434\u0430\u0433\u0443\u0432\u0430\u043d\u043d\u0456 \u043f\u0440\u043e\u0444\u0456\u043b\u044e: %s", e)
        driver.save_screenshot("edit_profile_error.png")
        raise

@pytest.mark.selenium
def test_calculate_relationship(driver, app, live_server):
    """
    Тестує калькулятор відносин між типами.
    
    Цей тест:
    1. Відкриває головну сторінку
    2. Входить як користувач
    3. Вибирає типи для порівняння
    4. Виконує розрахунок і перевіряє результат
    """
    with app.app_context():
        # Створюємо тестового користувача в базі даних
        from app.models import User
        from app.extensions import db
        
        test_username = unique_username("selenium_calc")
        test_email = unique_email("selenium_calc", "test.com")
        test_password = "TestPassword123!"
        
        user = User(username=test_username, email=test_email)
        user.set_password(test_password)
        db.session.add(user)
        db.session.commit()
    
    live_server_url = live_server.url
    
    try:
        # Відкриваємо сторінку входу і входимо
        driver.get(f"{live_server_url}/login")
        driver.find_element(By.ID, "email").send_keys(test_email)
        driver.find_element(By.ID, "password").send_keys(test_password)
        driver.find_element(By.ID, "submit").click()
        
        # На головній сторінці повинна бути форма розрахунку
        # Обираємо типологію (наприклад, "Temporistics")
        typology_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "typology"))
        )
        Select(typology_select).select_by_visible_text("1. Temporistics")
        
        # Обираємо типи для порівняння
        # Чекаємо, поки JavaScript заповнить опції
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#user1 option"))
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#user2 option"))
        )
        
        user1_select = Select(driver.find_element(By.ID, "user1"))
        user2_select = Select(driver.find_element(By.ID, "user2"))
        
        # Обираємо різні типи
        user1_select.select_by_index(0)  # Перший тип
        user2_select.select_by_index(1)  # Другий тип
        
        # Натискаємо кнопку розрахунку
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        
        # Перевіряємо, що результат відображається
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".result"))
        )
        
        # Перевіряємо, що результат містить інформацію про відносини
        result_text = driver.find_element(By.CSS_SELECTOR, ".result").text
        assert "Relationship Type:" in result_text or "Тип відносин:" in result_text
        
        logger.info("\u2713 \u0420\u043e\u0437\u0440\u0430\u0445\u0443\u043d\u043e\u043a \u0432\u0456\u0434\u043d\u043e\u0441\u0438\u043d \u043c\u0456\u0436 \u0442\u0438\u043f\u0430\u043c\u0438 \u043f\u0440\u043e\u0439\u0448\u043e\u0432 \u0443\u0441\u043f\u0456\u0448\u043d\u043e")
        
    except Exception as e:
        logger.error("\u041f\u043e\u043c\u0438\u043b\u043a\u0430 \u043f\u0440\u0438 \u0440\u043e\u0437\u0440\u0430\u0445\u0443\u043d\u043a\u0443 \u0432\u0456\u0434\u043d\u043e\u0441\u0438\u043d: %s", e)
        driver.save_screenshot("calculate_relationship_error.png")
        raise

@pytest.mark.selenium
def test_nearby_compatibles(driver, app, live_server, test_db):
    """
    Тестує функцію пошуку сумісних користувачів поблизу.
    
    Цей тест:
    1. Створює декілька користувачів з різними координатами і типами
    2. Входить як один з користувачів
    3. Перевіряє, що список сумісних користувачів відображається коректно
    """
    with app.app_context():
        # Створюємо кілька тестових користувачів з різними координатами
        from app.models import User, UserType
        from app.extensions import db
        
        # Створюємо основного користувача (Київ)
        main_username = unique_username("selenium_main")
        main_email = unique_email("selenium_main", "test.com")
        main_password = "TestPassword123!"
        
        # Тип для основного користувача - Temporistics
        main_type = UserType(
            typology_name="Temporistics",
            type_value="Past, Current, Future, Eternity"
        )
        db.session.add(main_type)
        db.session.flush()
        
        main_user = User(
            username=main_username, 
            email=main_email,
            latitude=50.4501,  # Київ
            longitude=30.5234,
            max_distance=1000,  # км
            type_id=main_type.id
        )
        main_user.set_password(main_password)
        db.session.add(main_user)
        
        # Сумісний користувач 1 (Львів, ~470 км)
        compatible1_type = UserType(
            typology_name="Temporistics",
            type_value="Current, Past, Future, Eternity"  # Сумісний тип
        )
        db.session.add(compatible1_type)
        db.session.flush()
        
        compatible1_username = unique_username("selenium_comp1")
        compatible1 = User(
            username=compatible1_username,
            email=unique_email("selenium_comp1", "test.com"),
            latitude=49.8397,  # Львів
            longitude=24.0297,
            type_id=compatible1_type.id
        )
        db.session.add(compatible1)
        
        # Сумісний користувач 2 (Одеса, ~440 км)
        compatible2_type = UserType(
            typology_name="Temporistics",
            type_value="Past, Future, Current, Eternity"  # Сумісний тип
        )
        db.session.add(compatible2_type)
        db.session.flush()
        
        compatible2_username = unique_username("selenium_comp2")
        compatible2 = User(
            username=compatible2_username,
            email=unique_email("selenium_comp2", "test.com"),
            latitude=46.4825,  # Одеса
            longitude=30.7233,
            type_id=compatible2_type.id
        )
        db.session.add(compatible2)
        
        # Несумісний користувач (Харків, ~410 км, але несумісний тип)
        incompatible_type = UserType(
            typology_name="Temporistics",
            type_value="Eternity, Future, Current, Past"  # Несумісний тип
        )
        db.session.add(incompatible_type)
        db.session.flush()
        
        incompatible = User(
            username=unique_username("selenium_incomp"),
            email=unique_email("selenium_incomp", "test.com"),
            latitude=49.9935,  # Харків
            longitude=36.2304,
            type_id=incompatible_type.id
        )
        db.session.add(incompatible)
        
        db.session.commit()
    
    live_server_url = live_server.url
    
    try:
        # Відкриваємо сторінку входу і входимо
        driver.get(f"{live_server_url}/login")
        driver.find_element(By.ID, "email").send_keys(main_email)
        driver.find_element(By.ID, "password").send_keys(main_password)
        driver.find_element(By.ID, "submit").click()
        
        # Переходимо на сторінку сумісних поблизу
        nearby_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/nearby_compatibles')]"))
        )
        nearby_link.click()
        
        # Перевіряємо, що сторінка завантажилася
        WebDriverWait(driver, 10).until(
            EC.url_contains("/nearby_compatibles")
        )
        
        # Перевіряємо текст сторінки на наявність імен сумісних користувачів
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Перевіряємо, що сумісні користувачі присутні в тексті сторінки
        assert compatible1_username in page_text, f"Сумісний користувач 1 ({compatible1_username}) не знайдений на сторінці"
        assert compatible2_username in page_text, f"Сумісний користувач 2 ({compatible2_username}) не знайдений на сторінці"
        
        logger.info("\u2713 \u0424\u0443\u043d\u043a\u0446\u0456\u044f \u043f\u043e\u0448\u0443\u043a\u0443 \u0441\u0443\u043c\u0456\u0441\u043d\u0438\u0445 \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0456\u0432 \u043f\u043e\u0431\u043b\u0438\u0437\u0443 \u043f\u0440\u0430\u0446\u044e\u0454 \u043a\u043e\u0440\u0435\u043a\u0442\u043d\u043e")
        
    except Exception as e:
        logger.error("\u041f\u043e\u043c\u0438\u043b\u043a\u0430 \u043f\u0440\u0438 \u0442\u0435\u0441\u0442\u0443\u0432\u0430\u043d\u043d\u0456 \u043f\u043e\u0448\u0443\u043a\u0443 \u0441\u0443\u043c\u0456\u0441\u043d\u0438\u0445 \u043a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0456\u0432: %s", e)
        driver.save_screenshot("nearby_compatibles_error.png")
        raise

@pytest.mark.selenium
def test_profile_image_upload(driver, app, live_server, test_db):
    """
    Тестує завантаження зображення профілю.
    
    Цей тест:
    1. Створює користувача і входить
    2. Відкриває сторінку редагування профілю
    3. Завантажує зображення
    4. Перевіряє успішність завантаження
    """
    with app.app_context():
        # Створюємо тестового користувача в базі даних
        from app.models import User
        from app.extensions import db

        test_username = unique_username("selenium_image")
        test_email = unique_email("selenium_image", "test.com")
        test_password = "TestPassword123!"

        user = User(username=test_username, email=test_email)
        user.set_password(test_password)
        db.session.add(user)
        db.session.commit()

    live_server_url = live_server.url

    try:
        # Відкриваємо сторінку входу і входимо
        driver.get(f"{live_server_url}/login")
        driver.find_element(By.ID, "email").send_keys(test_email)
        driver.find_element(By.ID, "password").send_keys(test_password)
        driver.find_element(By.ID, "submit").click()

        # Переходимо безпосередньо на сторінку редагування профілю
        driver.get(f"{live_server_url}/edit_profile")

        # Перевіряємо, що сторінка завантажилася
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "profile_image"))
        )

        # Створюємо тимчасовий файл для зображення
        import tempfile
        import os
        from PIL import Image

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as test_image:
            # Створюємо тестове зображення
            image = Image.new('RGB', (100, 100), color='red')
            image.save(test_image.name)
            test_image.flush()

            try:
                # Завантажуємо зображення
                file_input = driver.find_element(By.ID, "profile_image")
                file_input.send_keys(test_image.name)

                # Заповнюємо інші обов'язкові поля форми
                username_field = driver.find_element(By.ID, "username")
                username_field.clear()
                username_field.send_keys(test_username)

                email_field = driver.find_element(By.ID, "email")
                email_field.clear()
                email_field.send_keys(test_email)

                typology_field = driver.find_element(By.ID, "typology_name")
                typology_field.clear()
                typology_field.send_keys("Temporistics")

                type_field = driver.find_element(By.ID, "type_value")
                type_field.clear()
                type_field.send_keys("Past, Current, Future, Eternity")

                latitude_field = driver.find_element(By.ID, "latitude")
                latitude_field.clear()
                latitude_field.send_keys("50.4501")

                longitude_field = driver.find_element(By.ID, "longitude")
                longitude_field.clear()
                longitude_field.send_keys("30.5234")

                # Відправляємо форму
                driver.find_element(By.ID, "submit").click()

                # Перевіряємо, що повернулися на сторінку профілю
                WebDriverWait(driver, 10).until(
                    EC.url_contains(f"/user/{test_username}")
                )

                # Перевіряємо, що є повідомлення про успішне оновлення
                page_source = driver.page_source
                assert "Profile updated successfully" in page_source, "Повідомлення про успішне оновлення не відображається"

                logger.info("\u2713 \u0417\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0435\u043d\u043d\u044f \u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u043d\u044f \u043f\u0440\u043e\u0444\u0456\u043b\u044e \u043f\u0440\u043e\u0439\u0448\u043b\u043e \u0443\u0441\u043f\u0456\u0448\u043d\u043e")

            finally:
                # Видаляємо тимчасове зображення
                if os.path.exists(test_image.name):
                    os.remove(test_image.name)

    except Exception as e:
        logger.error("\u041f\u043e\u043c\u0438\u043b\u043a\u0430 \u043f\u0440\u0438 \u0437\u0430\u0432\u0430\u043d\u0442\u0430\u0436\u0435\u043d\u043d\u0456 \u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u043d\u044f \u043f\u0440\u043e\u0444\u0456\u043b\u044e: %s", e)
        driver.save_screenshot("image_upload_error.png")
        raise 