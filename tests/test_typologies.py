import pytest
from app.typologies.typology_temporistics import TypologyTemporistics


@pytest.fixture
def typology(app):
    with app.app_context():
        return TypologyTemporistics()


# Додайте ваші тести тут, використовуючи фікстуру typology
