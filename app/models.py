from . import db
from flask_login import UserMixin
from passlib.hash import bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey


# Модель User
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    type_id = Column(Integer, ForeignKey("user_type.id"))
    
    # Устанавливаем relationship, чтобы можно было сразу передавать user_type при создании
    user_type = db.relationship("UserType", backref="users")

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

