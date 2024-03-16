from flask import Flask
from config import config_dict

def create_app(config_name=None):
    """
    Create a Flask application using the app factory pattern.

    :param config_name: Configuration name (str)
    :return: Flask app
    """
    app = Flask(__name__)
    
    # Use the configuration specified by 'config_name' or default to 'development'
    config_name = config_name or 'development'
    app.config.from_object(config_dict.get(config_name))

    # Register Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Return the application instance
    return app
