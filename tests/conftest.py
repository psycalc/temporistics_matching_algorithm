# tests/conftest.py
import pytest
import os
import subprocess
import time
from app import create_app, db
from flask_migrate import upgrade

@pytest.fixture(scope="session", autouse=True)
def docker_compose_up(request):
    subprocess.run(["docker-compose", "up", "-d"], check=True)
    # Increase sleep if DB initialization takes longer
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
        # Ensure a clean database schema before running migrations
        # Drop all tables if any exist (in case a previous test run left them behind)
        db.session.remove()
        db.drop_all()
        # Now run migrations on a clean schema
        upgrade()  # Applies all migrations to the test database
    yield application

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function", autouse=True)
def transaction_rollback_fixture(app):
    # For each test, start a transaction and roll it back after test is done.
    with app.app_context():
        connection = db.engine.connect()
        trans = connection.begin()
        db.session.bind = connection
        yield
        trans.rollback()
        connection.close()
        db.session.remove()
