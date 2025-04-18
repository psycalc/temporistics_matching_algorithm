#!/bin/bash

# Додавання поточної директорії до PYTHONPATH
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Отримуємо IP адресу контейнера PostgreSQL
POSTGRES_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' temporistics_matching_algorithm-db-1 2>/dev/null || echo "localhost")

# Встановлення змінної середовища для використання тестової бази даних PostgreSQL
export USE_TEST_DB_URL="postgresql://testuser:password@$POSTGRES_HOST:5432/testdb"

# Запуск тестів Selenium
python -m pytest -xvs -m selenium tests/test_selenium_localization.py 