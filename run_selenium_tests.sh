#!/bin/bash

# Add the current directory to PYTHONPATH
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Obtain the IP address of the PostgreSQL container
POSTGRES_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' temporistics_matching_algorithm-db-1 2>/dev/null || echo "localhost")

# Set the environment variable for the test database URL
export USE_TEST_DB_URL="postgresql://testuser:password@$POSTGRES_HOST:5432/testdb"

# Run Selenium tests
python -m pytest -xvs -m selenium tests/test_selenium_localization.py
