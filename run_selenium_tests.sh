#!/bin/bash

# Додавання поточної директорії до PYTHONPATH
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Встановлення змінної середовища для використання тестової бази даних
export USE_TEST_DB_URL="sqlite:///test.db"

# Запуск тестів Selenium
python -m pytest -xvs -m selenium tests/test_selenium_localization.py 