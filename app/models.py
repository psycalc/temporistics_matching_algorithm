from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Модель User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    types = db.relationship('UserType', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Модель для зберігання типів користувача
class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typology_name = db.Column(db.String(64), nullable=False)  # Назва типології, наприклад, 'Temporistics'
    type_value = db.Column(db.String(64), nullable=False)  # Сам тип, наприклад, 'Past' чи 'Future'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
