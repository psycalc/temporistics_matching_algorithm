from flask import Flask, request, g, current_app
from config import config_dict
from .extensions import db, migrate, cache  # <-- Вот тут!
from flask_login import LoginManager
from flask_babel import Babel, refresh
from flask_wtf.csrf import CSRFProtect
import os
import logging  # Додано для більш детального логування
import gettext
from .context_processors import inject_translation  # Імпортуємо контекстний процесор

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "info"
csrf = CSRFProtect()

def create_app(config_name=None):
    app = Flask(__name__)
    config_name = config_name or "development"
    app.config.from_object(config_dict.get(config_name))

    # Якщо ми в тестингу, відключаємо проброс исключений.
    if app.config.get("TESTING"):
        app.config["PROPAGATE_EXCEPTIONS"] = False
        # Set UPLOAD_FOLDER dynamically
        app.config["UPLOAD_FOLDER"] = os.path.join(app.instance_path, 'uploads')
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Налаштування шляху для перекладів
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
    app.logger.setLevel(logging.INFO)
    app.logger.info(f"BABEL_TRANSLATION_DIRECTORIES: {app.config.get('BABEL_TRANSLATION_DIRECTORIES')}")
    app.logger.info(f"BABEL_DEFAULT_LOCALE: {app.config.get('BABEL_DEFAULT_LOCALE')}")
    app.logger.info(f"LANGUAGES: {app.config.get('LANGUAGES')}")

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    csrf.init_app(app)
    
    babel = Babel(app)
    login_manager.init_app(app)

    # Настраиваем локаль
    def get_locale():
        # Спочатку перевіряємо наявність мови в cookies
        locale = request.cookies.get('locale')
        
        # Логування для діагностики
        current_app.logger.info(f"BABEL: Cookie locale: {locale}")
        current_app.logger.info(f"BABEL: Supported languages: {app.config['LANGUAGES']}")
        
        # Якщо мова є в cookies і вона підтримується
        if locale and locale in app.config['LANGUAGES']:
            g.locale = locale  # Встановлюємо поточну мову в глобальний контекст
            current_app.logger.info(f"BABEL: Using locale from cookie: {locale}")
            return locale
        
        # Якщо немає в cookies або не підтримується, використовуємо найкращу відповідність
        best_match = request.accept_languages.best_match(app.config["LANGUAGES"])
        current_app.logger.info(f"BABEL: Best match locale: {best_match}")
        g.locale = best_match or app.config['BABEL_DEFAULT_LOCALE']
        return g.locale

    # Використовуємо новий формат у Flask-Babel 4.0.0
    babel.locale_selector_func = get_locale

    # Додаємо перевірку локалі перед кожним запитом
    @app.before_request
    def check_locale():
        current_app.logger.info(f"Before request - Checking locale")
        locale = request.cookies.get('locale')
        if locale:
            current_app.logger.info(f"Found locale in cookie: {locale}")
            if locale in app.config['LANGUAGES']:
                g.locale = locale
                # Примусово оновлюємо переклади для поточного запиту
                refresh()
                current_app.logger.info(f"Set g.locale to: {g.locale} and refreshed translations")
            else:
                current_app.logger.warning(f"Cookie locale {locale} not in supported languages")
        else:
            current_app.logger.info("No locale cookie found")

    # Додаємо змінні в контекст Jinja для всіх шаблонів
    @app.context_processor
    def inject_globals():
        current_app.logger.info(f"Injecting globals with locale: {g.get('locale', app.config['BABEL_DEFAULT_LOCALE'])}")
        return {
            'locale': g.get('locale', app.config['BABEL_DEFAULT_LOCALE']),
            'languages': app.config['LANGUAGES']
        }

    # Додаємо наш власний контекстний процесор для перекладів
    app.context_processor(inject_translation)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Додати template context processor для мовних перемикачів
    @app.context_processor
    def inject_language_form():
        from flask_wtf import FlaskForm
        class LanguageForm(FlaskForm):
            pass
        return {'form': LanguageForm()}

    # Добавляем тестовый маршрут для вызова ошибки 500, только если TESTING=True
    if app.config.get("TESTING"):
        @app.route("/cause_500")
        def cause_500():
            raise RuntimeError("Test 500 error")

    from .errors import register_error_handlers
    register_error_handlers(app)

    # Импортируем модели после создания приложения
    from .models import User, UserType

    # Перевіряємо, що файли переводів доступні
    @app.route('/debug_translations')
    def debug_translations():
        import glob
        translations_info = {}
        
        # Перевіряємо translations директорію
        translations_dir = os.path.join(app.root_path, '..', 'translations')
        for locale in app.config['LANGUAGES']:
            locale_dir = os.path.join(translations_dir, locale, 'LC_MESSAGES')
            mo_files = glob.glob(os.path.join(locale_dir, '*.mo'))
            translations_info[f'translations/{locale}'] = mo_files
        
        # Перевіряємо locales директорію
        locales_dir = os.path.join(app.root_path, '..', 'locales')
        for locale in app.config['LANGUAGES']:
            locale_dir = os.path.join(locales_dir, locale, 'LC_MESSAGES')
            mo_files = glob.glob(os.path.join(locale_dir, '*.mo'))
            translations_info[f'locales/{locale}'] = mo_files
            
        return {'translations': translations_info, 
                'babel_dirs': app.config.get('BABEL_TRANSLATION_DIRECTORIES'),
                'current_locale': g.get('locale', app.config['BABEL_DEFAULT_LOCALE'])}

    return app
