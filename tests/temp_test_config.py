import os

# Налаштування для тестів
os.environ["DATABASE_URL"] = "sqlite:///test.db"
os.environ["FLASK_CONFIG"] = "testing" 