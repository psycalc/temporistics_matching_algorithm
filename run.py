import os
from flask import Flask
from app import create_app

# Load the configuration from the environment variable.
# This approach emphasizes security and flexibility, allowing different configurations based on the environment.
config_name = os.getenv('FLASK_CONFIG', 'development')
if not config_name:
    raise ValueError("FLASK_CONFIG environment variable not set.")

app = create_app(config_name)

if __name__ == "__main__":
    # Retrieve host and port from environment variables with default values.
    # This allows for flexible deployment configurations.
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = os.getenv('FLASK_RUN_PORT', '5000')

    # Validate if port is an integer
    try:
        port = int(port)
    except ValueError:
        raise ValueError("FLASK_RUN_PORT environment variable must be an integer.")

    # Run the Flask application with the specified host and port
    app.run(host=host, port=port, debug=app.config['DEBUG'])
