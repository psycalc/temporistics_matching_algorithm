from flask import flash, redirect, url_for, current_app
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import current_user, login_user
from sqlalchemy.orm.exc import NoResultFound
from .extensions import db
from .models import User, UserType

# Створюємо SQLAlchemy моделі для зберігання OAuth токенів
class OAuth:
    @staticmethod
    def register_oauth_blueprints(app):
        # Налаштування OAuth для Google
        google_blueprint = make_google_blueprint(
            client_id=app.config.get("GOOGLE_CLIENT_ID", "dummy-client-id"),
            client_secret=app.config.get("GOOGLE_CLIENT_SECRET", "dummy-client-secret"),
            scope=["profile", "email"],
            # SQLAlchemyStorage для зберігання OAuth токенів в базі даних
            storage=SQLAlchemyStorage(OAuth.get_token_model('google'), db.session, user=current_user)
        )
        
        # Налаштування OAuth для GitHub
        github_blueprint = make_github_blueprint(
            client_id=app.config.get("GITHUB_CLIENT_ID", "dummy-client-id"),
            client_secret=app.config.get("GITHUB_CLIENT_SECRET", "dummy-client-secret"),
            scope=["user:email"],
            # SQLAlchemyStorage для зберігання OAuth токенів в базі даних
            storage=SQLAlchemyStorage(OAuth.get_token_model('github'), db.session, user=current_user)
        )
        
        # Реєструємо blueprints
        app.register_blueprint(google_blueprint, url_prefix="/login")
        app.register_blueprint(github_blueprint, url_prefix="/login")
        
        # Реєструємо обробники подій
        oauth_authorized.connect(OAuth.handle_google_authorize, sender=google_blueprint)
        oauth_authorized.connect(OAuth.handle_github_authorize, sender=github_blueprint)
        oauth_error.connect(OAuth.handle_oauth_error)
    
    @staticmethod
    def get_token_model(provider):
        if provider == 'google':
            from .models_oauth import GoogleOAuth
            return GoogleOAuth
        elif provider == 'github':
            from .models_oauth import GitHubOAuth
            return GitHubOAuth
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    @staticmethod
    def handle_google_authorize(blueprint, token):
        if not token:
            flash("Не вдалося увійти через Google.", "danger")
            return False
            
        # Отримуємо інформацію про користувача з Google
        resp = google.get("/oauth2/v2/userinfo")
        if not resp.ok:
            flash("Не вдалося отримати інформацію про користувача з Google.", "danger")
            return False
            
        google_info = resp.json()
        google_user_id = google_info["id"]
        
        # Пошук чи створення користувача
        try:
            # Шукаємо користувача за Google ID
            user = User.query.filter_by(google_id=google_user_id).first()
            
            if not user:
                # Шукаємо по email
                user = User.query.filter_by(email=google_info["email"]).first()
                if user:
                    # Користувач існує, оновлюємо його Google ID
                    user.google_id = google_user_id
                    if not user.avatar_url and "picture" in google_info:
                        user.avatar_url = google_info["picture"]
                else:
                    # Створюємо нового користувача
                    user = User(
                        username=google_info["email"].split("@")[0],
                        email=google_info["email"],
                        google_id=google_user_id
                    )
                    if "picture" in google_info:
                        user.avatar_url = google_info["picture"]
                    
                    # Створюємо базовий тип користувача
                    user_type = UserType(
                        typology_name="Temporistics",
                        type_value="Past, Current, Future, Eternity"
                    )
                    db.session.add(user_type)
                    db.session.flush()
                    user.type_id = user_type.id
                    
                    db.session.add(user)
                
                db.session.commit()
            
            # Вхід користувача
            login_user(user)
            flash("Успішно увійшли через Google.", "success")
            return False  # Не зберігати токен в базу даних, бо ми керуємо цим вручну
            
        except Exception as e:
            current_app.logger.error(f"Error processing Google OAuth: {str(e)}")
            flash("Сталася помилка при вході через Google.", "danger")
            return False
    
    @staticmethod
    def handle_github_authorize(blueprint, token):
        if not token:
            flash("Не вдалося увійти через GitHub.", "danger")
            return False
            
        # Отримуємо інформацію про користувача з GitHub
        resp = github.get("/user")
        if not resp.ok:
            flash("Не вдалося отримати інформацію про користувача з GitHub.", "danger")
            return False
            
        github_info = resp.json()
        github_user_id = str(github_info["id"])
        
        # Отримуємо email користувача (який може бути приватним)
        email_resp = github.get("/user/emails")
        if not email_resp.ok:
            flash("Не вдалося отримати email з GitHub.", "danger")
            return False
        
        emails = email_resp.json()
        primary_emails = [email for email in emails if email.get("primary")]
        email = primary_emails[0]["email"] if primary_emails else emails[0]["email"]
        
        # Пошук чи створення користувача
        try:
            # Шукаємо користувача за GitHub ID
            user = User.query.filter_by(github_id=github_user_id).first()
            
            if not user:
                # Шукаємо по email
                user = User.query.filter_by(email=email).first()
                if user:
                    # Користувач існує, оновлюємо його GitHub ID
                    user.github_id = github_user_id
                    if not user.avatar_url and "avatar_url" in github_info:
                        user.avatar_url = github_info["avatar_url"]
                else:
                    # Створюємо нового користувача
                    # Для username використовуємо login з GitHub або першу частину email
                    username = github_info.get("login") or email.split("@")[0]
                    
                    # Перевіряємо унікальність username
                    if User.query.filter_by(username=username).first():
                        username = f"{username}_{github_user_id[-6:]}"
                        
                    user = User(
                        username=username,
                        email=email,
                        github_id=github_user_id
                    )
                    if "avatar_url" in github_info:
                        user.avatar_url = github_info["avatar_url"]
                    
                    # Створюємо базовий тип користувача
                    user_type = UserType(
                        typology_name="Temporistics",
                        type_value="Past, Current, Future, Eternity"
                    )
                    db.session.add(user_type)
                    db.session.flush()
                    user.type_id = user_type.id
                    
                    db.session.add(user)
                
                db.session.commit()
            
            # Вхід користувача
            login_user(user)
            flash("Успішно увійшли через GitHub.", "success")
            return False  # Не зберігати токен в базу даних, бо ми керуємо цим вручну
            
        except Exception as e:
            current_app.logger.error(f"Error processing GitHub OAuth: {str(e)}")
            flash("Сталася помилка при вході через GitHub.", "danger")
            return False
    
    @staticmethod
    def handle_oauth_error(blueprint, error, error_description=None, error_uri=None):
        msg = f"OAuth error from {blueprint.name}! "
        if error_description:
            msg += f" Description: {error_description}"
        msg += f" Error: {error}"
        
        current_app.logger.error(msg)
        flash(f"Помилка при вході через {blueprint.name}: {error}", "danger") 