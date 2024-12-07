from . import db
from flask_login import UserMixin
from passlib.hash import bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy import event
from app.services import get_typology_instance



# Модель User
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)  # Добавить это поле
    type_id = Column(Integer, ForeignKey("user_type.id"))
    user_type = db.relationship("UserType", backref="users")

    # Новые поля для геолокации
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)



# Модель для зберігання типів користувача
class UserType(db.Model):
    __tablename__ = "user_type"
    id = db.Column(db.Integer, primary_key=True)
    typology_name = db.Column(db.String(50), nullable=False)
    type_value = db.Column(db.String(50), nullable=False)
    # user_id УБРАТЬ!

def validate_user_type(mapper, connection, target):
    # target это экземпляр UserType, который мы пытаемся вставить или обновить.
    typology_instance = get_typology_instance(target.typology_name)
    if not typology_instance:
        raise ValueError(f"Unknown typology: {target.typology_name}")

    all_types = typology_instance.get_all_types()
    if target.type_value not in all_types:
        raise ValueError(
            f"Invalid type_value '{target.type_value}' for typology '{target.typology_name}'"
        )

event.listen(UserType, 'before_insert', validate_user_type)
event.listen(UserType, 'before_update', validate_user_type)
