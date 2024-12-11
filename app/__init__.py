from flask import Flask, request
from config import config_dict
from .extensions import db, migrate, cache  # <-- Вот тут!
from flask_login import LoginManager
from flask_babel import Babel
import os

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "info"

def create_app(config_name=None):
    app = Flask(__name__)
    config_name = config_name or "development"
    app.config.from_object(config_dict.get(config_name))

    # Если мы в тестинге, отключаем проброс исключений.
    if app.config.get("TESTING"):
        app.config["PROPAGATE_EXCEPTIONS"] = False
        # Set UPLOAD_FOLDER dynamically
        app.config["UPLOAD_FOLDER"] = os.path.join(app.instance_path, 'uploads')
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

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

    # Добавляем тестовый маршрут для вызова ошибки 500, только если TESTING=True
    if app.config.get("TESTING"):
        @app.route("/cause_500")
        def cause_500():
            raise RuntimeError("Test 500 error")

    from .errors import register_error_handlers
    register_error_handlers(app)

    # Импортируем модели после создания приложения
    from .models import User, UserType

    # Теперь, когда модели импортированы, создадим таблицы.
    # Важно делать это в контексте приложения
    # with app.app_context():
    #     db.create_all()

    return app
