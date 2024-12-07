import patch_flask_babelplus
from flask import Flask, request
from config import config_dict
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler
from .services import cache
from flask_babel import Babel
from flask_login import LoginManager
from passlib.hash import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "info"

def create_app(config_name=None):
    app = Flask(__name__)
    config_name = config_name or "development"
    app.config.from_object(config_dict.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    babel = Babel(app)
    login_manager.init_app(app)

    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    )
    handler = RotatingFileHandler("app.log", maxBytes=10000000, backupCount=5)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    if app.config["DEBUG"]:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    def get_locale():
        return request.accept_languages.best_match(app.config["LANGUAGES"])

    babel.locale_selector_func = get_locale

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .errors import register_error_handlers
    register_error_handlers(app)

    # Импортируем модели после создания приложения
    from .models import User, UserType

    # Теперь, когда модели импортированы, создадим таблицы.
    # Важно делать это в контексте приложения
    # with app.app_context():
    #     db.create_all()

    return app
