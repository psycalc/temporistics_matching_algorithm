# config.py
import os
from dotenv import load_dotenv

# Загрузим переменные окружения из файла .env, который лежит в корне проекта
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "you-will-never-guess")
    # Підтримка як звичайного URL, так і Docker URL (для контейнерів)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DOCKER_DATABASE_URL", os.environ.get("DATABASE_URL", "postgresql://testuser:password@localhost:5432/testdb"))
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
    # Використовуємо PostgreSQL для тестів
    # Спочатку перевіряємо USE_TEST_DB_URL, потім DATABASE_URL, інакше використовуємо localhost
    SQLALCHEMY_DATABASE_URI = os.environ.get("USE_TEST_DB_URL", 
                            os.environ.get("DATABASE_URL", 
                            "postgresql://testuser:password@localhost:5432/testdb"))
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
