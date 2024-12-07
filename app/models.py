from . import db
from flask_login import UserMixin
from passlib.hash import bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float


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

