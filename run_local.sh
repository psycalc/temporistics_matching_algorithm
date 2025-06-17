#!/bin/bash

# Wrapper to run the application and optional tests locally.
# Usage: ./run_local.sh [options]
#
# Options:
#   --no-tests             Start the app without running tests
#   --tests-only           Run tests without starting the app
#   --exit-first           Stop on first failing test
#   --all-tests            Run all tests including selenium
#   --all-tests-exit-first Run all tests and stop on first failure

RUN_TESTS=true
RUN_APP=true
EXIT_FIRST=false
ALL_TESTS=false

for arg in "$@"; do
    case $arg in
        --no-tests)
            RUN_TESTS=false
            ;;
        --tests-only)
            RUN_APP=false
            RUN_TESTS=true
            ;;
        --exit-first)
            EXIT_FIRST=true
            ;;
        --all-tests-exit-first)
            ALL_TESTS=true
            EXIT_FIRST=true
            ;;
        --all-tests)
            ALL_TESTS=true
            ;;
    esac
done

check_port() {
    local port=$1
    lsof -i :"$port" | grep -q LISTEN
}

export FLASK_CONFIG=development
export BABEL_DEFAULT_LOCALE=en
export BABEL_DEFAULT_TIMEZONE=Europe/Kiev
export LANGUAGES=en,fr,es,uk
export BABEL_TRANSLATION_DIRECTORIES="translations;locales"
export FLASK_RUN_PORT=5001

app_running=false
if check_port "$FLASK_RUN_PORT"; then
    echo "App already running on port $FLASK_RUN_PORT"
    app_running=true
fi

POSTGRES_HOST=$(python scripts/check_db.py) || exit 1
export DATABASE_URL="postgresql://testuser:password@$POSTGRES_HOST:5432/testdb"

echo "Using PostgreSQL host: $POSTGRES_HOST"

if [ "$RUN_TESTS" = true ] && { [ "$RUN_APP" = false ] || [ "$app_running" = false ]; }; then
    EXIT_FIRST=$EXIT_FIRST ALL_TESTS=$ALL_TESTS python scripts/run_tests.py
    tests_result=$?
    if [ "$RUN_APP" = false ]; then
        exit $tests_result
    fi
    [ $tests_result -ne 0 ] && exit $tests_result
fi

if [ "$RUN_APP" = true ] && [ "$app_running" = false ]; then
    mkdir -p app/static/uploads instance
    echo "Starting the app on port $FLASK_RUN_PORT..."
    python run.py
else
    if [ "$RUN_TESTS" = true ] && [ "$app_running" = true ]; then
        EXIT_FIRST=$EXIT_FIRST ALL_TESTS=$ALL_TESTS python scripts/run_tests.py
    fi
fi

