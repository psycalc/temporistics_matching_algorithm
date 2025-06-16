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
    CHAT_PROVIDER = os.environ.get("CHAT_PROVIDER", "openai")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    HUGGINGFACE_MODEL = os.environ.get("HUGGINGFACE_MODEL", "google/flan-t5-small")
    HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-pro")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    LOCAL_MODEL_PATH = os.environ.get("LOCAL_MODEL_PATH")

    # Session security defaults
    SESSION_COOKIE_SECURE = settings.get("SESSION_COOKIE_SECURE", False)
    SESSION_COOKIE_HTTPONLY = settings.get("SESSION_COOKIE_HTTPONLY", True)
    SESSION_COOKIE_SAMESITE = settings.get("SESSION_COOKIE_SAMESITE", "Lax")

    # Content Security Policy for Talisman
    CONTENT_SECURITY_POLICY = "default-src 'self'"
    TALISMAN_FORCE_HTTPS = False

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
    # Require explicit secrets in production
    SECRET_KEY = settings.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = settings.get(
        "DOCKER_DATABASE_URL", settings.get("DATABASE_URL")
    )
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    TALISMAN_FORCE_HTTPS = True

    @staticmethod
    def init_app(app):
        if not app.config.get("SECRET_KEY"):
            raise RuntimeError("SECRET_KEY must be set in production")
        if not app.config.get("SQLALCHEMY_DATABASE_URI"):
            raise RuntimeError("DATABASE_URL must be set in production")

config_dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
