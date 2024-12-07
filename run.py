import os
import logging
from flask import Flask
from app import create_app, db
from flask_migrate import Migrate

logging.basicConfig(level=logging.INFO)  # Set up logging

config_name = os.getenv("FLASK_CONFIG", "development")
app = create_app(config_name)
migrate = Migrate(app, db)

if __name__ == "__main__":
    if app.config["DEBUG"]:
        logging.warning(
            "Running in DEBUG mode. Make sure this is not enabled in production!"
        )
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = os.getenv("FLASK_RUN_PORT", "5000")

    try:
        port = int(port)
    except ValueError:
        logging.error("FLASK_RUN_PORT environment variable must be an integer.")
        raise

    app.run(host=host, port=port, debug=app.config["DEBUG"])
