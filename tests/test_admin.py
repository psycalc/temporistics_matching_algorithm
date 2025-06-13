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


def test_distribution_page(client, app, test_db):
    with app.app_context():
        username = unique_username('dist')
        email = unique_email('dist')
        from app.models import UserType
        ut = UserType(typology_name='Temporistics', type_value='Past, Current, Future, Eternity')
        db.session.add(ut)
        db.session.flush()
        user = User(username=username, email=email, city='Kyiv', country='Ukraine', type_id=ut.id)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        login_user(client, email, 'password')
        response = client.get('/admin/distribution', follow_redirects=True)
        assert response.status_code == 200
        assert b'Type Distribution' in response.data

