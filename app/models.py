from .extensions import db
from flask_login import UserMixin
from passlib.hash import bcrypt
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy import event
from app.services import get_typology_instance



class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=True)  # Змінюємо на nullable=True, бо при OAuth пароль може бути не потрібен
    type_id = Column(Integer, ForeignKey("user_type.id"))
    user_type = db.relationship("UserType", backref="users")
    profile_image = Column(String(200), nullable=True)

    # Add latitude/longitude fields since tests assume their presence
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)

    # Profession info
    profession = Column(String(120), nullable=True)
    profession_visible = Column(Boolean, default=True)
    
    # Додаємо поле для зберігання максимальної прийнятної відстані (в км)
    max_distance = Column(Float, nullable=True, default=50.0)
    
    # Поля для OAuth
    google_id = Column(String(256), nullable=True, unique=True)
    github_id = Column(String(256), nullable=True, unique=True)
    # Можемо додати url аватару з соціальних мереж
    avatar_url = Column(String(512), nullable=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return bcrypt.verify(password, self.password_hash)


class UserType(db.Model):
    __tablename__ = "user_type"
    id = db.Column(db.Integer, primary_key=True)
    typology_name = db.Column(db.String(50), nullable=False)
    type_value = db.Column(db.String(50), nullable=False)

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

# Функція валідації координат користувача
def validate_user_coordinates(mapper, connection, target):
    # Перевіримо, що latitude і longitude є числами
    if target.latitude is not None:
        try:
            # Переконаємося, що це дійсно число
            target.latitude = float(target.latitude)
        except (ValueError, TypeError):
            # Якщо не вдається перетворити в число, встановлюємо None
            target.latitude = None
    
    if target.longitude is not None:
        try:
            # Переконаємося, що це дійсно число
            target.longitude = float(target.longitude)
        except (ValueError, TypeError):
            # Якщо не вдається перетворити в число, встановлюємо None
            target.longitude = None
    
    # Валідуємо максимальну відстань
    if target.max_distance is not None:
        try:
            # Переконуємося, що це дійсно число
            target.max_distance = float(target.max_distance)
            # Перевіряємо, що відстань не від'ємна
            if target.max_distance < 0:
                target.max_distance = 50.0  # Значення за замовчуванням
        except (ValueError, TypeError):
            # Якщо не вдається перетворити в число, встановлюємо значення за замовчуванням
            target.max_distance = 50.0

event.listen(UserType, 'before_insert', validate_user_type)
event.listen(UserType, 'before_update', validate_user_type)

# Додаємо обробники подій для валідації координат
event.listen(User, 'before_insert', validate_user_coordinates)
event.listen(User, 'before_update', validate_user_coordinates)
