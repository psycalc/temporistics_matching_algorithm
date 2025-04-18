# config.py
import os
from dotenv import load_dotenv

# Загрузим переменные окружения из файла .env, который лежит в корне проекта
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "you-will-never-guess")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
    BABEL_DEFAULT_LOCALE = os.environ.get("BABEL_DEFAULT_LOCALE", "en")
    BABEL_DEFAULT_TIMEZONE = os.environ.get("BABEL_DEFAULT_TIMEZONE", "UTC")
    LANGUAGES = os.environ.get("LANGUAGES", "en,fr,es,uk").split(",")
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    # Завжди використовуємо SQLite для тестів, щоб не залежати від PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get("USE_TEST_DB_URL", "sqlite:///test.db")
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
