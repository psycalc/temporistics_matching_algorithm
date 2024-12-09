# tests/conftest.py
import pytest
import os
import subprocess
import time
from app import create_app, db

@pytest.fixture(scope="session", autouse=True)
def docker_compose_up(request):
    subprocess.run(["docker-compose", "up", "-d"], check=True)
    time.sleep(20)
    def docker_compose_down():
        subprocess.run(["docker-compose", "down"], check=True)
    request.addfinalizer(docker_compose_down)

@pytest.fixture(scope="session")
def db_url():
    return os.environ.get("DATABASE_URL", "postgresql://user:password@localhost:5432/testdb")

@pytest.fixture(scope="session")
def app(db_url):
    application = create_app("testing")
    # Настраиваем тестовую БД
    application.config["SQLALCHEMY_DATABASE_URI"] = db_url
    application.config["TESTING"] = True
    with application.app_context():
        db.create_all()  # создаём таблицы один раз за сессию
    yield application
    # После всех тестов можно дропнуть (по желанию)
    # with application.app_context():
    #     db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function", autouse=True)
def transaction_rollback_fixture(app):
    # Для каждого теста создаём контекст приложения
    with app.app_context():
        # Начинаем транзакцию
        connection = db.engine.connect()
        trans = connection.begin()
        db.session.bind = connection

        yield

        # По окончании теста откатываем транзакцию
        trans.rollback()
        connection.close()
        db.session.remove()
