import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'simple'  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 300
    BABEL_DEFAULT_LOCALE = 'en'  # Add default locale
    BABEL_DEFAULT_TIMEZONE = 'UTC'  # Add default timezone
    LANGUAGES = ['en', 'fr', 'es']  # Add this line for available languages

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'

config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
