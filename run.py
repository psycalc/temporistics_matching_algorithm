import os
import logging
from app import create_app
from app.extensions import db
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

logging.basicConfig(level=logging.INFO)  # Set up logging

config_name = os.getenv("FLASK_CONFIG", "development")
app = create_app(config_name)
migrate = Migrate(app, db)

# Функція для отримання IP-адреси клієнта
def get_ip_key():
    return get_remote_address()

# Виправлення налаштувань лімітера для уникнення попередження
limiter = Limiter(
    app,
    key_func=get_ip_key,
    default_limits=["200 per day", "50 per hour"]
)

if __name__ == "__main__":
    if app.config["DEBUG"]:
        logging.warning(
            "Running in DEBUG mode. Make sure this is not enabled in production!"
        )
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = os.getenv("FLASK_RUN_PORT", "5000")

    try:
        port = int(port)
    except ValueError:
        logging.error("FLASK_RUN_PORT environment variable must be an integer.")
        raise

    app.run(host=host, port=port, debug=app.config["DEBUG"])
