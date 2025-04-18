# Psychological Calculator Project

**Table of Contents:**
1. [Project Description](#project-description)
2. [Theoretical Foundations](#theoretical-foundations)
    - [Temporistics (Time)](#temporistics-time)
    - [Psychosophy (Personality Aspects)](#psychosophy-personality-aspects)
    - [Socionics (Modeling of Information)](#socionics-modeling-of-information)
3. [Implementation in Code](#implementation-in-code)
    - [Typology Classes](#typology-classes)
    - [Services and Data Validation](#services-and-data-validation)
    - [Routes and Forms](#routes-and-forms)
4. [Testing](#testing)
5. [Installation and Run](#installation-and-run)
    - [Локальний запуск](#локальний-запуск)
    - [Запуск у Docker](#запуск-у-docker)
    - [Запуск тестів](#запуск-тестів)
6. [Additional Information](#additional-information)

---

## Project Description

This project integrates theoretical concepts from three typologies (Temporistics, Psychosophy, and Socionics) and implements them in a web application. Users can select their types, calculate relationships between types, and view the "comfort score" of these interactions.

The main goal is to demonstrate how theoretical models of perception (time, personality aspects, information) can be transformed into practical code, tested thoroughly, and presented through a web interface.

## Theoretical Foundations

### Temporistics (Time)
- **Four aspects:** Past, Current, Future, Eternity.
- **Induction vs. Deduction:**
  - Positions 1 & 4: Deductive (acting based on a preformed overall picture of time).
  - Positions 2 & 3: Inductive (collecting and analyzing information about time).

Conflict arises when one person operates deductively from a big-picture principle, while another uses induction, gathering data and adapting continuously.

### Psychosophy (Personality Aspects)
- **Four aspects:** Emotion, Logic, Will, Physics.
- **Analysis vs. Synthesis:**
  - Positions 1 & 4: Synthetic (holistic perception of the aspect).
  - Positions 2 & 3: Analytic (breaking the aspect down into components).

Conflict: a synthetic individual acts holistically without dissecting details, while an analytic individual seeks to break everything down and understand each part.

### Socionics (Modeling of Information)
- Focuses on logical, ethical, sensory, and intuitive modeling of information.
- Each type perceives and processes information differently:
  - The logician uses systems and structures,
  - The ethicist focuses on emotional exchange,
  - The sensor relies on tangible, concrete reality,
  - The intuit deals with abstract concepts and possibilities.

Conflict: Different types struggle to "mirror" or understand the other's model of perception.

## Implementation in Code

### Typology Classes
Under `app/typologies/`, each typology is implemented as a class derived from an abstract `Typology`. They provide methods like:
- `get_all_types()` to retrieve all types.
- `shorten_type()` to abbreviate type names.
- `determine_relationship_type()` to calculate the relationship type between two given types.
- `get_comfort_score()` to determine a "comfort score" based on their relationship.

These methods directly reflect the theoretical principles: induction/deduction (Temporistics), analysis/synthesis (Psychosophy), and modeling (Socionics).

### Services and Data Validation
`services.py` contains:
- `get_types_by_typology()`: returns type lists according to the chosen typology class.
- `calculate_relationship(user1, user2, typology)`: applies typology logic to determine relationship type and comfort score.

`models.py` holds `User` and `UserType` models. User types are validated before insertion, ensuring no invalid type values are saved. This enforces theoretical constraints at the database level.

### Routes and Forms
`routes.py` ties logic to the web interface:
- `/calculate`: users submit two types and a typology to get a result.
- `/register`: users choose their types from dynamically loaded lists of available typologies.

`forms.py` manages forms for registration, login, and profile editing. The form fields and validations are driven by the theoretical concepts implemented in the classes.

## Testing
Tests ensure the theory is correctly implemented:
- `tests/test_typologies.py`: checks typology logic — from retrieving types to determining relationships and handling errors.
- `tests/test_routes.py`: verifies user flows, including login, registration, language changes, and calculation endpoints.
- `tests/test_services.py`: ensures `calculate_relationship()` and `get_types_by_typology()` work as intended.
- `tests/test_models.py`: tests database logic and `UserType` validation.
- `tests/test_errors.py`: confirms correct handling of 404 and 500 errors.

A high test coverage (~93%) confirms that the theoretical ideas are correctly mirrored in code and thoroughly tested.

## Installation and Run

### Локальний запуск

1. **Підготовка**:
   - Переконайтеся, що у вас встановлено Python 3.10 або новіше
   - Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```

2. **Налаштування середовища**:
   - Створіть файл `.env` у корені проекту (якщо його ще немає)
   - Налаштуйте необхідні змінні середовища (приклад):
   ```
   FLASK_CONFIG=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///site.db  # Для розробки можна використовувати SQLite
   BABEL_DEFAULT_LOCALE=uk
   BABEL_DEFAULT_TIMEZONE=Europe/Kiev
   LANGUAGES=en,fr,es,uk
   ```

3. **Запуск сервера розробки**:
   
   Спосіб 1: Використання скрипта `run_local.sh` (рекомендовано):
   ```bash
   chmod +x run_local.sh  # надання прав на виконання (лише один раз)
   ./run_local.sh
   ```
   
   Скрипт автоматично:
   - Налаштовує середовище для роботи з SQLite (база даних буде створена в корені проекту)
   - Створює необхідні директорії
   - Перевіряє наявність прав на запис файлу бази даних
   - Ініціалізує базу даних, якщо вона не існує
   - Запускає додаток на порту 5001 (щоб уникнути конфліктів) 
   
   Спосіб 2: Прямий запуск:
   ```bash
   python run.py
   ```
   
   Додаток буде доступний за адресою http://localhost:5001 (якщо використовується скрипт) або http://localhost:5000 (при прямому запуску).
   
   > **Можливі проблеми та їх вирішення**:
   > 
   > 1. **Помилка про підключення до PostgreSQL**: Якщо ви бачите помилку про неможливість підключення до хоста "db", використовуйте скрипт `run_local.sh` або встановіть змінну середовища `DATABASE_URL` на SQLite.
   > 
   > 2. **Помилка "Порт вже використовується"**: Для вирішення можна:
   >    - Змінити порт у скрипті `run_local.sh` (змінна `FLASK_RUN_PORT`)
   >    - Знайти і зупинити процес, що використовує порт: `sudo lsof -i :5000` та `sudo kill <PID>`
   >
   > 3. **Помилка SQLite "unable to open database file"**:
   >    - Перевірте права доступу до директорії проекту: `ls -la`
   >    - Запустіть скрипт з актуальної версії, яка створює базу даних у корені проекту
   >    - Спробуйте запустити з підвищеними привілеями: `sudo ./run_local.sh`

### Запуск у Docker

1. **Використання Docker Compose**:
   ```bash
   docker-compose up
   ```
   Цей команда запустить базу даних PostgreSQL та веб-додаток.

2. **Запуск тільки веб-додатку**:
   ```bash
   docker-compose up web
   ```

### Запуск тестів

#### Основні команди для запуску тестів

1. **Налаштування середовища для тестів**:
   ```bash
   export PYTHONPATH="$PYTHONPATH:$(pwd)"
   export USE_TEST_DB_URL="sqlite:///test.db" 
   export FLASK_CONFIG=testing
   ```

2. **Запуск усіх тестів**:
   ```bash
   python -m pytest
   ```

3. **Запуск конкретного тесту**:
   ```bash
   python -m pytest tests/test_localization.py::test_language_affects_content
   ```

4. **Запуск тестів із певного файлу**:
   ```bash
   python -m pytest tests/test_models.py
   ```

5. **Запуск тестів із більш детальним виводом**:
   ```bash
   python -m pytest -xvs tests/test_localization.py
   ```

6. **Запуск Selenium тестів**:
   ```bash
   python -m pytest -m selenium
   ```
   
   Для запуску Selenium тестів переконайтеся, що у вас встановлено:
   - Chrome браузер
   - ChromeDriver (відповідної версії)

#### Альтернативний запуск тестів через скрипт

Для тестів Selenium можна використовувати скрипт:
```bash
bash run_selenium_tests.sh
```

#### Запуск тестів у Docker

```bash
docker-compose up test
```

#### Примітки щодо тестування

- Для тестів використовується SQLite замість PostgreSQL, щоб уникнути залежності від зовнішньої бази даних.
- Під час запуску тестів створюються тимчасові таблиці, які видаляються після виконання тестів.
- Якщо ви змінюєте структуру бази даних, переконайтеся, що ви також оновили відповідні тести.
- Високий рівень покриття тестами (~93%) підтверджує, що теоретичні ідеї проекту коректно реалізовані у коді.

## Additional Information

This project is developed by [Your Name] and is licensed under the [License Name].

For more information, please visit the project repository on [GitHub](https://github.com/yourusername/psychological-calculator) or contact the developer at [your.email@example.com].
