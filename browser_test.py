#!/usr/bin/env python3

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Перелік текстів, які мають бути присутні на сторінці для кожної мови
EXPECTED_TEXTS = {
    "en": ["Login", "Register"],
    "fr": ["Connexion", "S'inscrire"],
    "es": ["Iniciar sesión", "Registrarse"], 
    "uk": ["Увійти", "Зареєструватися"]
}

def setup_driver():
    """Налаштування веб-драйвера."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск у фоновому режимі без вікна
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Ініціалізуємо веб-драйвер
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        print(f"Помилка встановлення ChromeDriverManager: {e}")
        try:
            # Для випадків, коли ChromeDriverManager не працює
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Помилка створення драйвера Chrome: {e}")
            sys.exit(1)
    
    # Встановлюємо неявне очікування
    driver.implicitly_wait(10)
    return driver

def test_language_switcher(url):
    """
    Перевіряє, що перемикач мов працює правильно.
    
    Цей тест:
    1. Відкриває головну сторінку сайту
    2. Перемикає мову за допомогою вибору в селекті
    3. Перевіряє, що зміст сторінки змінився відповідно до обраної мови
    4. Повторює для всіх підтримуваних мов
    """
    driver = setup_driver()
    
    try:
        # Відвідуємо головну сторінку
        driver.get(url)
        print(f"Відкрито сторінку: {url}")
        
        # Для кожної підтримуваної мови
        for lang in ["en", "uk", "fr", "es"]:
            print(f"\nТестуємо мову: {lang}")
            
            try:
                # Знаходимо селектор мови
                language_select = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "languageSelect"))
                )
                print(f"✓ Знайдено селектор мови")
                
                # Вибираємо опцію за значенням мови
                driver.execute_script(f"document.getElementById('languageSelect').value = '{lang}';")
                driver.execute_script("submitLanguageForm();")
                print(f"✓ Обрано мову '{lang}' через JavaScript")
                
                # Даємо час для перезавантаження сторінки
                time.sleep(2)
                
                # Перевіряємо, що cookie "locale" встановлено
                cookies = driver.get_cookies()
                locale_cookie = next((cookie for cookie in cookies if cookie["name"] == "locale"), None)
                
                if locale_cookie is not None:
                    print(f"✓ Cookie 'locale' встановлено: {locale_cookie['value']}")
                    if locale_cookie["value"] == lang:
                        print(f"✓ Значення cookie правильне: {locale_cookie['value']}")
                    else:
                        print(f"✗ Значення cookie неправильне: {locale_cookie['value']} (очікувалося: {lang})")
                else:
                    print(f"✗ Cookie 'locale' не встановлено для мови {lang}")
                
                # Перевіряємо, що тексти на сторінці відображаються правильною мовою
                if lang in EXPECTED_TEXTS:
                    page_source = driver.page_source
                    all_texts_found = True
                    
                    for expected_text in EXPECTED_TEXTS[lang]:
                        if expected_text in page_source:
                            print(f"✓ Знайдено текст '{expected_text}'")
                        else:
                            print(f"✗ Не знайдено текст '{expected_text}'")
                            all_texts_found = False
                    
                    if all_texts_found:
                        print(f"✓ Всі очікувані тексти знайдено для мови {lang}")
                    else:
                        print(f"✗ Деякі очікувані тексти не знайдено для мови {lang}")
                else:
                    print(f"? Немає очікуваних текстів для тестування мови {lang}")
                
            except Exception as e:
                print(f"✗ Помилка при тестуванні мови {lang}: {e}")
        
    finally:
        # Закриваємо браузер після тесту
        driver.quit()
        print("\nТестування завершено.")

def test_login_form(url):
    """
    Перевіряє, що форма входу відображається правильно на різних мовах.
    """
    driver = setup_driver()
    
    try:
        # Словник з очікуваними текстами для форми входу на різних мовах
        login_texts = {
            "en": ["Log In", "Email", "Password"],
            "fr": ["Connexion", "Courriel", "Mot de passe"],
            "es": ["Iniciar sesión", "Correo electrónico", "Contraseña"],
            "uk": ["Увійти", "Електронна пошта", "Пароль"]
        }
        
        # Для кожної мови перевіряємо форму логіну
        for lang in ["en", "uk", "fr", "es"]:
            if lang not in login_texts:
                continue
                
            print(f"\nТестуємо форму входу для мови: {lang}")
            
            try:
                # Відвідуємо сторінку логіну
                driver.get(f"{url}/login")
                print(f"✓ Відкрито сторінку входу: {url}/login")
                
                # Вибираємо мову
                language_select = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "languageSelect"))
                )
                print(f"✓ Знайдено селектор мови")
                
                driver.execute_script(f"document.getElementById('languageSelect').value = '{lang}';")
                driver.execute_script("submitLanguageForm();")
                print(f"✓ Обрано мову '{lang}' через JavaScript")
                
                time.sleep(2)
                
                # Перевіряємо, що тексти форми входу відображаються правильною мовою
                page_source = driver.page_source
                all_texts_found = True
                
                for expected_text in login_texts[lang]:
                    if expected_text in page_source:
                        print(f"✓ Знайдено текст '{expected_text}'")
                    else:
                        print(f"✗ Не знайдено текст '{expected_text}'")
                        all_texts_found = False
                
                if all_texts_found:
                    print(f"✓ Всі очікувані тексти форми входу знайдено для мови {lang}")
                else:
                    print(f"✗ Деякі очікувані тексти форми входу не знайдено для мови {lang}")
                
            except Exception as e:
                print(f"✗ Помилка при тестуванні форми входу для мови {lang}: {e}")
    
    finally:
        # Закриваємо браузер після тесту
        driver.quit()
        print("\nТестування форми входу завершено.")

if __name__ == "__main__":
    # Встановлюємо URL сайту (за замовчуванням - локальний сервер)
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "http://localhost:5000"
    
    print(f"Тестування локалізації для сайту: {url}")
    test_language_switcher(url)
    test_login_form(url) 