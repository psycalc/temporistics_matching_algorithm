# entrypoint.sh
#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
flask db upgrade

# Start the application
echo "Starting application..."
exec "$@"
