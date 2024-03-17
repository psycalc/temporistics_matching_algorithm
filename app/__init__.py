from flask import Flask
from config import config_dict
import logging
from logging.handlers import RotatingFileHandler

def create_app(config_name=None):
    """
    Create a Flask application using the app factory pattern.

    :param config_name: Configuration name (str)
    :return: Flask app
    """
    app = Flask(__name__)

    # Use the configuration specified by 'config_name' or default to 'development'
    config_name = config_name or 'development'
    app.config.from_object(config_dict.get(config_name))

    # Configure logging
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Set the appropriate log level based on the configuration
    if app.config['DEBUG']:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    # Register Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Return the application instance
    return app