import os
import sys
import logging
from flask import Flask, request, g, url_for
from datetime import datetime
from config import config_dict
from flask_babel import Babel, _
from dotenv import load_dotenv
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect

# Загрузимо змінні оточення з .env файлу
load_dotenv()
cache = Cache()
babel = Babel()
csrf = CSRFProtect()

def create_app(config_name="development"):
    app = Flask(__name__)
    
    # Визначаємо конфігурацію
    if config_name not in config_dict:
        app.logger.warning(f"Unknown configuration: {config_name}, using development instead")
        config_name = "development"
    
    # Застосовуємо конфігурацію
    app.config.from_object(config_dict[config_name])
    
    # Налаштування OAuth для локальної розробки
    if config_name == "development":
        app.config["GOOGLE_CLIENT_ID"] = os.environ.get("GOOGLE_CLIENT_ID")
        app.config["GOOGLE_CLIENT_SECRET"] = os.environ.get("GOOGLE_CLIENT_SECRET")
        app.config["GITHUB_CLIENT_ID"] = os.environ.get("GITHUB_CLIENT_ID")
        app.config["GITHUB_CLIENT_SECRET"] = os.environ.get("GITHUB_CLIENT_SECRET")
        app.config["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Дозволяє використовувати OAuth без HTTPS
    
    # Мультимовність
    app.logger.info(f"BABEL_TRANSLATION_DIRECTORIES: {app.config.get('BABEL_TRANSLATION_DIRECTORIES', 'translations')}")
    app.logger.info(f"BABEL_DEFAULT_LOCALE: {app.config.get('BABEL_DEFAULT_LOCALE', 'en')}")
    app.logger.info(f"LANGUAGES: {app.config.get('LANGUAGES', ['en'])}")
    
    # Ініціалізуємо розширення
    from app.extensions import db, migrate, login_manager
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Для тестів використовуємо інший тип кешу
    if config_name == 'testing':
        app.config['CACHE_TYPE'] = 'NullCache'  # Вимикаємо кешування в тестах
    
    cache.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Регіструємо blueprint'и
    from app.routes import main
    from app.admin import admin_bp
    app.register_blueprint(main)
    app.register_blueprint(admin_bp)
    
    # Ініціалізуємо OAuth, окрім тестового оточення. У тестах залежність
    # flask-dance може бути відсутня, тому пропускаємо реєстрацію OAuth
    if config_name != 'testing':
        try:
            from app.oauth import OAuth
            OAuth.register_oauth_blueprints(app)
        except ModuleNotFoundError:
            app.logger.warning(
                "flask-dance is not installed; skipping OAuth blueprint registration"
            )
    
    # Debug налаштування
    if app.debug:
        logging.warning("Running in DEBUG mode. Make sure this is not enabled in production!")
        
    # Зберігаємо URL додатку для генерації URL-ів у задачах
    app.config['APPLICATION_ROOT'] = '/'
    
    # Додаємо глобальний обробник запитів щоб встановити локаль
    @app.before_request
    def before_request():
        app.logger.info("Before request - Checking locale")
        locale = request.cookies.get('locale')
        
        if locale is None:
            locale = request.accept_languages.best_match(app.config['LANGUAGES'])
            if locale is None:
                locale = app.config['BABEL_DEFAULT_LOCALE']
            app.logger.info(f"No locale in cookie, using accept-language or default: {locale}")
        else:
            app.logger.info(f"Found locale in cookie: {locale}")
            
        g.locale = locale
        app.logger.info(f"Set g.locale to: {locale} and refreshed translations")
    
    # Налаштовуємо обробник для login_manager
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Додаємо тестовий маршрут для перевірки помилки 500
    @app.route("/cause_500")
    def cause_500():
        # Спеціально створюємо помилку для тестування обробки 500 помилок
        raise RuntimeError("Test 500 error")
    
    # Імпортуємо і реєструємо обробники помилок
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    return app
