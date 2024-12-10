# tests/conftest.py
import pytest
import os
from app import create_app, db
from flask_migrate import Migrate, upgrade

migrate = Migrate()

@pytest.fixture(scope="session")
def db_url():
    return os.environ.get("DATABASE_URL", "postgresql://testuser:password@db:5432/testdb")

@pytest.fixture(scope="session")
def app(db_url):
    application = create_app("testing")
    application.config["SQLALCHEMY_DATABASE_URI"] = db_url
    application.config["TESTING"] = True
    with application.app_context():
        migrate.init_app(application, db)
        upgrade()
        # Создаём таблицы, которых нет в миграциях (например, user_type)
        db.create_all()
    yield application

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
