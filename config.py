# config.py
import os
from dynaconf import Dynaconf

# Dynaconf автоматично завантажує .env та змінні оточення
settings = Dynaconf(envvar_prefix=False, load_dotenv=True)

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = settings.get("SECRET_KEY", "you-will-never-guess")
    # Підтримка як звичайного URL, так і Docker URL (для контейнерів)
    SQLALCHEMY_DATABASE_URI = settings.get("DOCKER_DATABASE_URL", settings.get("DATABASE_URL", "postgresql://testuser:password@localhost:5432/testdb"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
    BABEL_DEFAULT_LOCALE = settings.get("BABEL_DEFAULT_LOCALE", "en")
    BABEL_DEFAULT_TIMEZONE = settings.get("BABEL_DEFAULT_TIMEZONE", "UTC")
    LANGUAGES = settings.get("LANGUAGES", "en,fr,es,uk").split(",")
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')

class DevelopmentConfig(Config):
    DEBUG = True
    GOOGLE_CLIENT_ID = settings.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = settings.get("GOOGLE_CLIENT_SECRET")
    GITHUB_CLIENT_ID = settings.get("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = settings.get("GITHUB_CLIENT_SECRET")
    OAUTHLIB_INSECURE_TRANSPORT = "1"

class TestingConfig(Config):
    TESTING = True
    # Використовуємо PostgreSQL для тестів
    # Спочатку перевіряємо USE_TEST_DB_URL, потім DATABASE_URL, інакше використовуємо localhost
    SQLALCHEMY_DATABASE_URI = settings.get(
        "USE_TEST_DB_URL",
        settings.get(
            "DATABASE_URL",
            "postgresql://testuser:password@localhost:5432/testdb",
        ),
    )
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "testsecretkey"
    # Використовуємо окрему папку для тестових завантажень
    UPLOAD_FOLDER = os.path.join(basedir, 'tests', 'uploads')

class ProductionConfig(Config):
    DEBUG = False

config_dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
