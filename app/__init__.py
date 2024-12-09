from flask import Flask, request
from config import config_dict
from .extensions import db, migrate, cache  # <-- Вот тут!
from flask_login import LoginManager
from flask_babel import Babel

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

    # Настраиваем локаль
    def get_locale():
        return request.accept_languages.best_match(app.config["LANGUAGES"])
    babel.locale_selector_func = get_locale

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .errors import register_error_handlers
    register_error_handlers(app)

    return app
