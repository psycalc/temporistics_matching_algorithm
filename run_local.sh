#!/bin/bash

# Local helper script to run the application and tests.
# Supports running all tests with optional early exit on first failure.
# Usage: ./run_local.sh [options]
#
# Examples:
#   ./run_local.sh                     - start the app and basic tests
#   ./run_local.sh --tests-only        - run only the basic tests
#   ./run_local.sh --all-tests         - run all tests including selenium
#   ./run_local.sh --all-tests-exit-first - run all tests and stop on first failure
#   ./run_local.sh --exit-first        - run basic tests and stop on first failure

# Check if a process is already listening on the given port
check_port() {
    local port=$1
    local process_count=$(lsof -i :$port | grep -v "COMMAND" | wc -l)
    if [ $process_count -gt 0 ]; then
        return 0 # Port in use
    else
        return 1 # Port available
    fi
}

# Check whether the PostgreSQL Docker container is running
check_db_container() {
    local container_count=$(docker ps | grep "postgres" | wc -l)
    if [ $container_count -gt 0 ]; then
        return 0 # Container running
    else
        return 1 # Container not running
    fi
}

# Attempt to connect to PostgreSQL
check_postgres_connection() {
    # Try local connection first
    if psql -h localhost -U testuser -d testdb -c "SELECT 1" > /dev/null 2>&1; then
        echo "Successfully connected to PostgreSQL via localhost."
        export DATABASE_URL="postgresql://testuser:password@localhost:5432/testdb"
        return 0
    # Then try using the service name "db"
    elif [ -n "$DOCKER_NETWORK" ] && psql -h db -U testuser -d testdb -c "SELECT 1" > /dev/null 2>&1; then
        echo "Successfully connected to PostgreSQL via container 'db'."
        export DATABASE_URL="postgresql://testuser:password@db:5432/testdb"
        return 0
    else
        echo "Failed to connect to PostgreSQL. Is the container running?"
        return 1
    fi
}

# Run the test suite
run_tests() {
    echo "=== Running tests ==="
    
    # Obtain the PostgreSQL container IP
    local POSTGRES_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' temporistics_matching_algorithm-db-1)
    echo "PostgreSQL container IP: $POSTGRES_HOST"
    
    # Configure the testing environment
    export PYTHONPATH="$PYTHONPATH:$(pwd)"
    
    # Use PostgreSQL for tests
    export USE_TEST_DB_URL="postgresql://testuser:password@localhost:5432/testdb"
    
    export FLASK_CONFIG=testing
    
    # Extra environment variables for localization and Selenium tests
    export BABEL_DEFAULT_LOCALE=en
    export BABEL_DEFAULT_TIMEZONE=Europe/Kiev
    export LANGUAGES=en,fr,es,uk
    export BABEL_TRANSLATION_DIRECTORIES="translations;locales"
    
    # Test run parameters
    PYTEST_ARGS="-v -s"  # verbose output (-v) and show print statements (-s)
    
    # Add early-exit parameter if requested
    if [ "$EXIT_FIRST" = true ]; then
        PYTEST_ARGS="$PYTEST_ARGS -x"
    fi
    
    if [ "$ALL_TESTS" = true ]; then
        echo "Running all tests (including selenium)..."
        python -m pytest $PYTEST_ARGS tests/
    else
        echo "Running default tests..."
        # Exclude selenium tests by default
        python -m pytest $PYTEST_ARGS -k "not selenium"
    fi
    
    TEST_EXIT_CODE=$?
    if [ $TEST_EXIT_CODE -eq 0 ]; then
        echo "✅ All tests passed!"
    else
        echo "❌ Some tests failed. Check the log above for details."
    fi
    
    return $TEST_EXIT_CODE
}

# Parse command line arguments
# Available options:
# --no-tests         - start only the app without tests
# --tests-only       - run tests without starting the app
# --exit-first       - stop on first failing test
# --all-tests        - run all tests including selenium
# --all-tests-exit-first - run all tests and stop on first failure

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

# Set environment variables for local development
export FLASK_CONFIG=development

# Localization settings
export BABEL_DEFAULT_LOCALE=en
export BABEL_DEFAULT_TIMEZONE=Europe/Kiev
export LANGUAGES=en,fr,es,uk
export BABEL_TRANSLATION_DIRECTORIES="translations;locales"

# Specify the port (default 5000 but can be changed)
export FLASK_RUN_PORT=5001

# Check if the app is already running
if check_port $FLASK_RUN_PORT; then
    echo "WARNING: The app is already running on port $FLASK_RUN_PORT!"
    echo "To stop it, find the PID: lsof -i :$FLASK_RUN_PORT"
    echo "Then run: kill <PID>"
    app_running=true
else
    app_running=false
fi

# Check if the database container is running
if check_db_container; then
    echo "PostgreSQL container is running. Checking connection..."
    db_running=true
else
    echo "PostgreSQL container not running. Starting..."
    db_running=false
fi

# Start the database container if not running
if [ "$db_running" = false ]; then
    echo "Starting PostgreSQL container..."
    docker-compose up -d db
    
    # Wait until the database is ready
    echo "Waiting for database connection..."
    sleep 5
    attempts=0
    max_attempts=10
    
    while ! docker-compose exec db psql -U testuser -d testdb -c "SELECT 1" > /dev/null 2>&1; do
        attempts=$((attempts + 1))
        if [ $attempts -ge $max_attempts ]; then
            echo "Failed to connect to the database after $max_attempts attempts."
            echo "Check your Docker and PostgreSQL settings."
            exit 1
        fi
        echo "Attempt $attempts of $max_attempts. Waiting 2 seconds..."
        sleep 2
    done
    
    echo "PostgreSQL database is up and ready!"
fi

# Get the PostgreSQL container IP for local connection
POSTGRES_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' temporistics_matching_algorithm-db-1)
if [ -n "$POSTGRES_HOST" ]; then
    echo "PostgreSQL container IP: $POSTGRES_HOST"
    # Set DATABASE_URL to connect to PostgreSQL
    export DATABASE_URL="postgresql://testuser:password@$POSTGRES_HOST:5432/testdb"
else
    echo "WARNING: Could not obtain PostgreSQL container IP!"
    echo "Using local database URL instead."
    export DATABASE_URL="postgresql://testuser:password@localhost:5432/testdb"
fi

# Run tests if requested and the app is not already running
if [ "$RUN_TESTS" = true ] && { [ "$RUN_APP" = false ] || [ "$app_running" = false ]; }; then
    run_tests
    tests_result=$?
    
    # Exit here when running only tests
    if [ "$RUN_APP" = false ]; then
        exit $tests_result
    fi
fi

# Start the application if it is not already running
if [ "$app_running" = false ] && [ "$RUN_APP" = true ]; then
    # Ensure directories for static files exist
    mkdir -p app/static/uploads
    mkdir -p instance
    
    # Start the main script
    echo "Starting the app with PostgreSQL on port $FLASK_RUN_PORT..."
    
    # If tests were run first, simply start the app
    if [ "$RUN_TESTS" = true ]; then
        python run.py
    else
        # Start the app in background and run tests if requested
        python run.py &
        APP_PID=$!
        
        # Give the app time to start
        echo "Waiting for the app to start..."
        sleep 5
        
        # Run tests if requested
        if [ "$RUN_TESTS" = true ]; then
            run_tests
            tests_result=$?
            
            # Stop the app if tests failed
            if [ $tests_result -ne 0 ]; then
                echo "Tests failed, stopping the app..."
                kill $APP_PID
                exit $tests_result
            fi
        fi
        
        # Wait while the app is running
        wait $APP_PID
    fi
else
    echo "The app is already running. To restart it:"
    echo "1. Stop the current process"
    echo "2. Run this script again"
    
    # Run tests if requested and they have not been executed yet
    if [ "$RUN_TESTS" = true ]; then
        run_tests
    fi
fi

echo "Script finished!"
