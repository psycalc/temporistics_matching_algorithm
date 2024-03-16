import os

class Config:
    """
    Base configuration class. Contains default configuration settings,
    plus configurations that are common to all environments.
    """
    # Security
    # It's critical to use an environment variable for the secret key and not provide a default.
    SECRET_KEY = os.environ['SECRET_KEY']  # Raises an error if the environment variable is not set, enhancing security.

    # Database modifications tracking - typically set to False to avoid overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Add other general configurations here

class DevelopmentConfig(Config):
    """
    Development configurations, inherits from Config.
    """
    DEBUG = True  # Enables debug mode for error tracking.

    # Development-specific configurations like database URI can be set here.
    # Example for SQLite:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    # Replace the above line with the appropriate database URI for your development environment.

    # Additional development-specific variables can be added here.

class TestingConfig(Config):
    """
    Testing configurations, inherits from Config.
    """
    TESTING = True  # Enables testing mode.
    
    # Test-specific configurations like database URI can be set here.
    # Example for SQLite:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    # Replace the above line with the correct database URI for your test environment.

    # Additional testing-specific variables can be added here.

class ProductionConfig(Config):
    """
    Production configurations, inherits from Config.
    """
    DEBUG = False  # Debug mode should be off in production.

    # Production-specific configurations like database URI should be set here.
    # It's a best practice to use environment variables for sensitive data.
    # Example:
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # Replace the above line with the correct environment variable for your production database URI.

    # Additional production-specific variables can be added here.

# You might define a dictionary to ease switching between configurations:
config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# Usage example in your main application file:
# app.config.from_object(config_dict[os.getenv('FLASK_CONFIG', 'development')])
