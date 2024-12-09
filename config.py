import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "you-will-never-guess")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
    BABEL_DEFAULT_LOCALE = os.environ.get("BABEL_DEFAULT_LOCALE", "en")
    BABEL_DEFAULT_TIMEZONE = os.environ.get("BABEL_DEFAULT_TIMEZONE", "UTC")
    LANGUAGES = os.environ.get("LANGUAGES", "en,fr,es").split(",")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    WTF_CSRF_ENABLED = False  # Важно для корректной работы тестов, чтобы не было проблем с CSRF
    SECRET_KEY = "testsecretkey"  # Явно задаём, чтобы флеш работал в тестах

class ProductionConfig(Config):
    DEBUG = False

config_dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
