import pytest
import os
import time
import uuid
import io
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
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
    
    try:
        print("Створення екземпляру Chrome за допомогою ChromeDriverManager")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except WebDriverException as e:
        print(f"Помилка при ініціалізації ChromeDriver: {e}")
        try:
            print("Спроба створення драйвера без ChromeDriverManager")
            driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException as e:
            print(f"Помилка при ініціалізації Chrome: {e}")
            raise
    
    print("ChromeDriver успішно ініціалізовано")
    
    # Встановлюємо неявне очікування
    driver.implicitly_wait(10)
    
    yield driver
    
    # Закриваємо браузер після тесту
    print("Закриваємо драйвер після тесту")
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
    print(f"URL тестового сервера: {live_server_url}")
    
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
        
        print(f"✓ Реєстрація користувача {test_username} пройшла успішно")
        
    except Exception as e:
        print(f"Помилка при реєстрації користувача: {e}")
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
        
        print(f"✓ Вхід користувача {test_username} пройшов успішно")
        
        # Тепер тестуємо вихід
        logout_link.click()
        
        # Перевіряємо, що перенаправлені на сторінку входу
        WebDriverWait(driver, 10).until(
            EC.url_contains("/login")
        )
        
        # Перевіряємо, що в меню є пункт "Login" після виходу
        login_link = driver.find_element(By.XPATH, "//a[contains(@href, '/login')]")
        assert login_link.is_displayed(), "Посилання для входу не знайдено після виходу"
        
        print(f"✓ Вихід користувача пройшов успішно")
        
    except Exception as e:
        print(f"Помилка при тестуванні входу/виходу: {e}")
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
        
        # Переходимо на сторінку редагування профілю
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/user/')]"))
        ).click()
        
        # Знаходимо посилання на редагування профілю
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Edit')]"))
        ).click()
        
        # Змінюємо дані профілю
        new_lat = "51.5074"  # Координати Лондона
        new_lon = "-0.1278"
        new_max_distance = "100.0"
        
        # Заповнюємо нові дані
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
        
        # Перевіряємо, що є повідомлення про успішне оновлення
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        
        # Перевіряємо, що повернулися на сторінку профілю
        assert f"/user/{test_username}" in driver.current_url, "Не перенаправлені на сторінку профілю після оновлення"
        
        print(f"✓ Редагування профілю користувача {test_username} пройшло успішно")
        
    except Exception as e:
        print(f"Помилка при редагуванні профілю: {e}")
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
        Select(typology_select).select_by_visible_text("Temporistics")
        
        # Даємо час для завантаження типів
        time.sleep(1)
        
        # Обираємо перший тип
        user1_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user1"))
        )
        Select(user1_select).select_by_index(0)
        
        # Обираємо другий тип
        user2_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user2"))
        )
        Select(user2_select).select_by_index(1)
        
        # Відправляємо форму
        calculate_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Calculate')]")
        calculate_button.click()
        
        # Перевіряємо, що результат відображається
        result_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        
        assert "Relationship Type:" in result_element.text, "Результат розрахунку не відображається"
        assert "Comfort Score:" in result_element.text, "Комфортність не відображається"
        
        print("✓ Розрахунок відносин між типами працює коректно")
        
    except Exception as e:
        print(f"Помилка при розрахунку відносин: {e}")
        driver.save_screenshot("calculate_error.png")
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
        
        compatible1 = User(
            username=unique_username("selenium_comp1"),
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
        
        compatible2 = User(
            username=unique_username("selenium_comp2"),
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
        
        # Перевіряємо, що обидва сумісних користувача присутні в списку
        user_elements = driver.find_elements(By.CLASS_NAME, "user-card")
        usernames = [elem.text for elem in user_elements]
        
        # Шукаємо у тексті сторінки
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        assert len(user_elements) >= 2, f"Знайдено менше 2 сумісних користувачів: {len(user_elements)}"
        assert compatible1.username in page_text, f"Сумісний користувач 1 не знайдений у списку"
        assert compatible2.username in page_text, f"Сумісний користувач 2 не знайдений у списку"
        assert incompatible.username not in page_text, f"Несумісний користувач знайдений у списку, але не повинен бути"
        
        print("✓ Функція пошуку сумісних користувачів поблизу працює коректно")
        
    except Exception as e:
        print(f"Помилка при тестуванні пошуку сумісних користувачів: {e}")
        driver.save_screenshot("nearby_error.png")
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
        
        # Переходимо на сторінку профілю
        profile_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/user/')]"))
        )
        profile_link.click()
        
        # Переходимо на сторінку редагування профілю
        edit_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Edit')]"))
        )
        edit_link.click()
        
        # Створюємо тимчасовий файл з зображенням
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            # Створюємо тестове зображення
            image = Image.new('RGB', (100, 100), color='red')
            image.save(temp_file.name)
            temp_filename = temp_file.name
        
        # Знаходимо поле вводу файлу і завантажуємо зображення
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "profile_image"))
        )
        file_input.send_keys(temp_filename)
        
        # Відправляємо форму
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()
        
        # Перевіряємо, що є повідомлення про успішне оновлення
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        assert "updated successfully" in success_message.text, "Повідомлення про успішне оновлення не знайдено"
        
        # Перевіряємо, що повернулися на сторінку профілю
        assert f"/user/{test_username}" in driver.current_url, "Не перенаправлені на сторінку профілю після оновлення"
        
        # Видаляємо тимчасовий файл
        os.unlink(temp_filename)
        
        print(f"✓ Завантаження зображення профілю для користувача {test_username} пройшло успішно")
        
    except Exception as e:
        print(f"Помилка при завантаженні зображення профілю: {e}")
        driver.save_screenshot("upload_image_error.png")
        # Якщо тимчасовий файл був створений, спробуємо його видалити
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.unlink(temp_filename)
        raise 