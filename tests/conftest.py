# tests/conftest.py
import pytest
import os
import sys
import tempfile
import random
import string
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base

from app import create_app
from app.extensions import db
from flask_migrate import Migrate, upgrade

from app.models import User, UserType
import pytest
import threading
import socket
from werkzeug.serving import make_server

# Створюємо екземпляр Migrate для тестування
migrate = Migrate()

@pytest.fixture(scope="session")
def db_url():
    """URL для з'єднання з базою даних."""
    env_url = os.environ.get("TEST_DB_URL")
    if env_url:
        return env_url

    db_type = os.environ.get("TEST_DB", "postgresql").lower()
    if db_type == "sqlite":
        return "sqlite:///:memory:"

    # Пробуємо спочатку підключитися через localhost, це працює надійніше в WSL2
    return "postgresql://testuser:password@localhost:5432/testdb"

@pytest.fixture(scope="session")
def app(db_url):
    application = create_app("testing")
    application.config["SQLALCHEMY_DATABASE_URI"] = db_url
    application.config["TESTING"] = True
    
    # Створюємо власний engine і таблиці для тестування
    engine = create_engine(db_url)
    metadata = MetaData()
    
    # Визначаємо таблиці
    users = Table('users', metadata,
        Column('id', Integer, primary_key=True),
        Column('username', String(80), unique=True),
        Column('email', String(120), unique=True),
        Column('password_hash', String(128), nullable=True),
        Column('type_id', Integer, ForeignKey('user_type.id')),
        Column('profile_image', String(200)),
        Column('latitude', Float),
        Column('longitude', Float),
        Column('max_distance', Float, default=50.0),
        Column('google_id', String(256), nullable=True),
        Column('github_id', String(256), nullable=True),
        Column('avatar_url', String(512), nullable=True)
    )
    
    user_type = Table('user_type', metadata,
        Column('id', Integer, primary_key=True),
        Column('typology_name', String(50)),
        Column('type_value', String(50))
    )
    
    # Створюємо таблиці
    with application.app_context():
        # Ініціалізуємо міграції
        migrate.init_app(application, db)
        metadata.create_all(engine)
    
    yield application

# Створюємо фікстуру для live_server
class LiveServer:
    def __init__(self, app, port):
        self.app = app
        self.port = port
        self.server = make_server('localhost', port, app)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def stop(self):
        self.server.shutdown()
        self.thread.join()

    @property
    def url(self):
        return f'http://localhost:{self.port}'

def get_free_port():
    """Знаходить вільний порт для запуску сервера."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 0))
        return s.getsockname()[1]

@pytest.fixture(scope='function')
def live_server(app):
    """Запускає тестовий сервер у окремому потоці та ініціалізує базу даних."""
    # Ініціалізуємо базу даних перед запуском сервера
    with app.app_context():
        print("Creating tables for LiveServer test...")
        db.create_all()  # Створюємо всі таблиці перед тестом
        
        # Перевіряємо, який тип бази даних використовується
        engine = db.engine
        dialect = engine.dialect.name
        
        # Для SQLAlchemy 2.0 потрібно використовувати text() для текстових запитів
        from sqlalchemy import text
        with engine.connect() as connection:
            if dialect == 'postgresql':
                result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
            elif dialect == 'sqlite':
                result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            else:
                raise ValueError(f"Unsupported database dialect: {dialect}")

            tables = [row[0] for row in result]
            print(f"Tables in LiveServer database ({dialect}): {tables}")

    # Запускаємо сервер
    port = get_free_port()
    server = LiveServer(app, port)
    server.start()
    yield server
    
    # Прибираємо за собою після завершення тесту
    with app.app_context():
        db.session.remove()
        db.drop_all()  # Видаляємо таблиці після тесту
        print("LiveServer tables dropped...")
    
    server.stop()

@pytest.fixture(scope="function")
def test_db(app):
    with app.app_context():
        print("Creating tables for test...")
        db.create_all()  # Створюємо всі таблиці перед тестом
        print("Tables created...")
        
        # Перевіряємо, який тип бази даних використовується
        engine = db.engine
        dialect = engine.dialect.name
        
        # Для SQLAlchemy 2.0 потрібно використовувати text() для текстових запитів
        from sqlalchemy import text
        with engine.connect() as connection:
            if dialect == 'postgresql':
                result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
            elif dialect == 'sqlite':
                result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            else:
                raise ValueError(f"Unsupported database dialect: {dialect}")

            tables = [row[0] for row in result]
            print(f"Tables in database ({dialect}): {tables}")
            
        yield db
        db.session.remove()
        db.drop_all()  # Видаляємо таблиці після тесту
        print("Tables dropped...")

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

# В тестах используем так:
# def test_something(client, app):
#    with app.app_context():
#        test_someting
#    assert ...

@pytest.fixture(scope="function")
def client_with_ctx(app, db):
    with app.app_context():
        yield app.test_client()
