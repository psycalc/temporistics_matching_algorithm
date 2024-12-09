import pytest
import os
import subprocess
import time
from app import create_app, db
from flask_migrate import upgrade

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
    application.config["SQLALCHEMY_DATABASE_URI"] = db_url
    application.config["TESTING"] = True
    with application.app_context():
        db.session.remove()
        db.drop_all()
        upgrade()  # Applies all migrations
    yield application

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

# transaction_rollback_fixture removed/commented out
