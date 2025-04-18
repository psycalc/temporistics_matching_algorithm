from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from .extensions import db
from .models import User

class GoogleOAuth(OAuthConsumerMixin, db.Model):
    __tablename__ = "google_oauth"
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
    
    # Додатково можна зберігати інші дані, специфічні для Google
    profile_id = db.Column(db.String(256), nullable=True)
    
class GitHubOAuth(OAuthConsumerMixin, db.Model):
    __tablename__ = "github_oauth"
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
    
    # Додатково можна зберігати інші дані, специфічні для GitHub
    login = db.Column(db.String(256), nullable=True) 