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
def app():
    # Создаём приложение в конфигурации "testing" (убедитесь, что такой конфиг существует)
    application = create_app("testing")

    # Здесь можно задать любые тестовые настройки
    # Например: application.config["TESTING"] = True

    with application.app_context():
        yield application
