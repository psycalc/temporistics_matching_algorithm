#!/bin/sh
set -e

echo "Container started"
echo "RUN_TESTS=$RUN_TESTS"

wait_for_db() {
    until pg_isready -h db -U postgres -t 10; do
        echo "Waiting for Postgres to be ready..."
        sleep 2
    done
}

if [ "$RUN_TESTS" = "1" ]; then
    export PATH="/root/.local/bin:$PATH"
    wait_for_db
    flask db upgrade
    exec pytest
else
    wait_for_db
    flask db upgrade  # Применяем миграции перед запуском сервера
    exec flask run --host="${FLASK_RUN_HOST:-127.0.0.1}"
fi
