import pytest
import uuid
from app import db
from app.models import User, UserType
import sqlalchemy.exc

def unique_username(prefix="testuser"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def unique_email(prefix="test", domain="example.com"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@{domain}"

def test_user_model(app):
    with app.app_context():
        username = unique_username("testuser_model")
        email = unique_email("test_model")
        user = User(username=username, email=email)
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username=username).first()
        assert retrieved_user is not None
        assert retrieved_user.email == email
        assert retrieved_user.check_password("testpassword")

def test_user_with_type(app):
    with app.app_context():
        user_type = UserType(
            typology_name="Temporistics",
            type_value="Past, Current, Future, Eternity"
        )
        db.session.add(user_type)
        db.session.commit()

        username = unique_username("typeuser")
        email = unique_email("typeuser")
        user = User(username=username, email=email, user_type=user_type)
        user.set_password("securepass")
        db.session.add(user)
        db.session.commit()

        retrieved = User.query.filter_by(username=username).first()
        assert retrieved is not None
        assert retrieved.user_type is not None
        assert retrieved.user_type.typology_name == "Temporistics"
        assert retrieved.user_type.type_value == "Past, Current, Future, Eternity"

def test_user_uniqueness(app):
    with app.app_context():
        base_username = unique_username("uniqueuser")
        email1 = unique_email("unique1")
        user1 = User(username=base_username, email=email1)
        user1.set_password("pass1")
        db.session.add(user1)
        db.session.commit()

        email2 = unique_email("unique2")
        user2 = User(username=base_username, email=email2)
        user2.set_password("pass2")
        db.session.add(user2)

        with pytest.raises(sqlalchemy.exc.IntegrityError):
            db.session.commit()
