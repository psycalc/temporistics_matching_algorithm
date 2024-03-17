from flask import Flask, request
from config import config_dict
import logging
from logging.handlers import RotatingFileHandler
from .services import cache
from flask_babel import Babel  # Add this for Babel
from flask import current_app  # Add this import at the beginning of your routes.py

def create_app(config_name=None):
    """
    Create a Flask application using the app factory pattern.
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

    # Initialize the Cache instance with the app
    cache.init_app(app)

    # Initialize Babel for internationalization
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        # Select a language translation that best fits the user's preferences
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    # Register Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
