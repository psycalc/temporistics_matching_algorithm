#!/bin/bash

# Скрипт для запуску додатку і тестів локально
# Підтримує запуск всіх тестів із зупинкою на першому поломаному тесті
# Використання: ./run_local.sh [опції]
#
# Приклади:
#   ./run_local.sh                     - запуск додатку і базових тестів
#   ./run_local.sh --tests-only        - запуск тільки базових тестів
#   ./run_local.sh --all-tests         - запуск всіх тестів, включаючи selenium
#   ./run_local.sh --all-tests-exit-first - запуск всіх тестів з зупинкою на першому поломаному
#   ./run_local.sh --exit-first        - запуск базових тестів з зупинкою на першому поломаному

# Функція для перевірки чи запущено процес на певному порту
check_port() {
    local port=$1
    local process_count=$(lsof -i :$port | grep -v "COMMAND" | wc -l)
    if [ $process_count -gt 0 ]; then
        return 0 # Порт зайнятий
    else
        return 1 # Порт вільний
    fi
}

# Функція для перевірки чи запущено Docker контейнер з базою даних
check_db_container() {
    local container_count=$(docker ps | grep "postgres" | wc -l)
    if [ $container_count -gt 0 ]; then
        return 0 # Контейнер запущено
    else
        return 1 # Контейнер не запущено
    fi
}

# Функція для перевірки з'єднання з PostgreSQL
check_postgres_connection() {
    # Спроба підключитися локально
    if psql -h localhost -U testuser -d testdb -c "SELECT 1" > /dev/null 2>&1; then
        echo "Підключення до PostgreSQL через localhost успішне."
        export DATABASE_URL="postgresql://testuser:password@localhost:5432/testdb"
        return 0
    # Спроба підключитися через ім'я сервісу "db"
    elif [ -n "$DOCKER_NETWORK" ] && psql -h db -U testuser -d testdb -c "SELECT 1" > /dev/null 2>&1; then
        echo "Підключення до PostgreSQL через контейнер db успішне."
        export DATABASE_URL="postgresql://testuser:password@db:5432/testdb"
        return 0
    else
        echo "Не вдалося підключитися до PostgreSQL. Перевірте, чи запущений контейнер."
        return 1
    fi
}

# Функція для запуску тестів
run_tests() {
    echo "=== Запуск тестів ==="
    
    # Отримуємо IP адресу контейнера PostgreSQL
    local POSTGRES_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' temporistics_matching_algorithm-db-1)
    echo "IP-адреса контейнера PostgreSQL: $POSTGRES_HOST"
    
    # Налаштування тестового середовища
    export PYTHONPATH="$PYTHONPATH:$(pwd)"
    
    # Використовуємо PostgreSQL для тестів
    export USE_TEST_DB_URL="postgresql://testuser:password@localhost:5432/testdb"
    
    export FLASK_CONFIG=testing
    
    # Додаткові змінні середовища для локалізації та Selenium-тестів
    export BABEL_DEFAULT_LOCALE=uk
    export BABEL_DEFAULT_TIMEZONE=Europe/Kiev
    export LANGUAGES=en,fr,es,uk
    export BABEL_TRANSLATION_DIRECTORIES="translations;locales"
    
    # Параметри запуску тестів
    PYTEST_ARGS="-v -s"  # детальний вивід (-v) і вивід print statements (-s)
    
    # Додаємо параметр зупинки на першій помилці, якщо потрібно
    if [ "$EXIT_FIRST" = true ]; then
        PYTEST_ARGS="$PYTEST_ARGS -x"
    fi
    
    if [ "$ALL_TESTS" = true ]; then
        echo "Запускаємо всі можливі тести (включаючи selenium)..."
        python -m pytest $PYTEST_ARGS tests/
    else
        echo "Запускаємо стандартні тести..."
        # Виключаємо selenium-тести за замовчуванням
        python -m pytest $PYTEST_ARGS -k "not selenium"
    fi
    
    TEST_EXIT_CODE=$?
    if [ $TEST_EXIT_CODE -eq 0 ]; then
        echo "✅ Всі тести успішно пройдені!"
    else
        echo "❌ Деякі тести не пройшли. Перевірте лог вище для деталей."
    fi
    
    return $TEST_EXIT_CODE
}

# Парсинг аргументів
# Доступні опції:
# --no-tests         - запустити тільки додаток без тестів
# --tests-only       - запустити тільки тести без додатку
# --exit-first       - зупинитися на першому поломаному тесті
# --all-tests        - запустити всі тести, включаючи selenium-тести
# --all-tests-exit-first - запустити всі тести і зупинитися на першому поломаному

RUN_TESTS=true
RUN_APP=true
EXIT_FIRST=false
ALL_TESTS=false

for arg in "$@"; do
    case $arg in
        --no-tests)
            RUN_TESTS=false
            shift
            ;;
        --tests-only)
            RUN_APP=false
            RUN_TESTS=true
            shift
            ;;
        --exit-first)
            EXIT_FIRST=true
            shift
            ;;
        --all-tests-exit-first)
            ALL_TESTS=true
            EXIT_FIRST=true
            shift
            ;;
        --all-tests)
            ALL_TESTS=true
            shift
            ;;
    esac
done

# Налаштовуємо змінні середовища для локальної розробки
export FLASK_CONFIG=development

# Локалізаційні налаштування
export BABEL_DEFAULT_LOCALE=uk
export BABEL_DEFAULT_TIMEZONE=Europe/Kiev
export LANGUAGES=en,fr,es,uk
export BABEL_TRANSLATION_DIRECTORIES="translations;locales"

# Вказуємо порт (за замовчуванням 5000, але можна змінити)
export FLASK_RUN_PORT=5001

# Перевіряємо чи додаток вже запущено
if check_port $FLASK_RUN_PORT; then
    echo "УВАГА: Додаток вже запущено на порту $FLASK_RUN_PORT!"
    echo "Щоб зупинити, знайдіть PID процесу: lsof -i :$FLASK_RUN_PORT"
    echo "Потім виконайте: kill <PID>"
    app_running=true
else
    app_running=false
fi

# Перевіряємо чи база даних вже запущена
if check_db_container; then
    echo "Контейнер з PostgreSQL запущено. Перевіряємо підключення..."
    db_running=true
else
    echo "Контейнер з PostgreSQL не запущено. Запускаємо..."
    db_running=false
fi

# Якщо база даних не запущена, обов'язково запускаємо її
if [ "$db_running" = false ]; then
    echo "Запускаємо контейнер з PostgreSQL..."
    docker-compose up -d db
    
    # Чекаємо поки база даних повністю запуститься
    echo "Очікування підключення до бази даних..."
    sleep 5
    attempts=0
    max_attempts=10
    
    while ! docker-compose exec db psql -U testuser -d testdb -c "SELECT 1" > /dev/null 2>&1; do
        attempts=$((attempts + 1))
        if [ $attempts -ge $max_attempts ]; then
            echo "Не вдалося підключитися до бази даних після $max_attempts спроб."
            echo "Перевірте налаштування Docker і PostgreSQL."
            exit 1
        fi
        echo "Спроба $attempts з $max_attempts. Очікуємо ще 2 секунди..."
        sleep 2
    done
    
    echo "База даних PostgreSQL успішно запущена та готова до роботи!"
fi

# Отримуємо IP адресу контейнера PostgreSQL для локального підключення
POSTGRES_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' temporistics_matching_algorithm-db-1)
if [ -n "$POSTGRES_HOST" ]; then
    echo "IP-адреса контейнера PostgreSQL: $POSTGRES_HOST"
    # Налаштовуємо змінну DATABASE_URL для підключення до PostgreSQL
    export DATABASE_URL="postgresql://testuser:password@$POSTGRES_HOST:5432/testdb"
else
    echo "УВАГА: Не вдалося отримати IP-адресу контейнера PostgreSQL!"
    echo "Використовуємо локальний URL для бази даних."
    export DATABASE_URL="postgresql://testuser:password@localhost:5432/testdb"
fi

# Запускаємо тести, якщо потрібно і ми не запускаємо додаток або додаток не запущено
if [ "$RUN_TESTS" = true ] && { [ "$RUN_APP" = false ] || [ "$app_running" = false ]; }; then
    run_tests
    tests_result=$?
    
    # Якщо ми запускаємо тільки тести - виходимо
    if [ "$RUN_APP" = false ]; then
        exit $tests_result
    fi
fi

# Якщо додаток не запущено і нам потрібно його запустити - запускаємо
if [ "$app_running" = false ] && [ "$RUN_APP" = true ]; then
    # Перевіряємо наявність каталогів для статичних файлів
    mkdir -p app/static/uploads
    mkdir -p instance
    
    # Запускаємо головний скрипт
    echo "Запускаємо додаток з PostgreSQL базою даних на порту $FLASK_RUN_PORT..."
    
    # Якщо тести вже запущені і нам потрібно запустити додаток після них
    if [ "$RUN_TESTS" = true ]; then
        python run.py
    else
        # Запускаємо додаток і тести, якщо потрібно
        python run.py &
        APP_PID=$!
        
        # Даємо додатку час на запуск
        echo "Очікуємо, поки додаток запуститься..."
        sleep 5
        
        # Запускаємо тести, якщо потрібно
        if [ "$RUN_TESTS" = true ]; then
            run_tests
            tests_result=$?
            
            # Зупиняємо додаток, якщо тести провалилися
            if [ $tests_result -ne 0 ]; then
                echo "Тести провалились, зупиняємо додаток..."
                kill $APP_PID
                exit $tests_result
            fi
        fi
        
        # Чекаємо, поки додаток працює
        wait $APP_PID
    fi
else
    echo "Додаток вже запущено. Якщо хочете перезапустити:"
    echo "1. Зупиніть поточний процес"
    echo "2. Запустіть скрипт знову"
    
    # Запускаємо тести, якщо потрібно і ми ще не запустили їх
    if [ "$RUN_TESTS" = true ]; then
        run_tests
    fi
fi

echo "Скрипт завершено!" 