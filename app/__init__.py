import patch_flask_babelplus
from flask import Flask, request
from config import config_dict
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
from .services import cache
from flask_babel  import Babel
from flask_login import LoginManager
from passlib.hash import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "info"


def create_app(config_name=None):
    """
    Create a Flask application using the app factory pattern.
    """
    app = Flask(__name__)

    # Use the configuration specified by 'config_name' or default to 'development'
    config_name = config_name or "development"
    app.config.from_object(config_dict.get(config_name))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    babel = Babel(app)
    login_manager.init_app(app)

    # Configure logging
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    )
    handler = RotatingFileHandler("app.log", maxBytes=10000000, backupCount=5)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Set the appropriate log level based on the configuration
    if app.config["DEBUG"]:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    @babel.localeselector
    def get_locale():
        # Select a language translation that best fits the user's preferences
        return request.accept_languages.best_match(app.config["LANGUAGES"])

    # Register Blueprints
    from .routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # Register error handlers
    from .errors import register_error_handlers

    register_error_handlers(app)

    return app
