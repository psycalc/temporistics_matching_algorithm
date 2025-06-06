import json
from app.extensions import db
from app.models import User
from tests.test_helpers import unique_username, unique_email


def login_user(client, email, password):
    client.post('/login', data={'email': email, 'password': password, 'submit': 'Login'}, follow_redirects=True)


def test_admin_page_access(client, app, test_db):
    with app.app_context():
        username = unique_username('admin')
        email = unique_email('admin')
        user = User(username=username, email=email)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        login_user(client, email, 'password')
        response = client.get('/admin/', follow_redirects=True)
        assert response.status_code == 200
        assert b'Typology Weights' in response.data
        assert b'Enable Typologies' in response.data

