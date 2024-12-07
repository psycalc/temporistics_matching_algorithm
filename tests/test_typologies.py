import pytest
from app.typologies.typology_temporistics import TypologyTemporistics


@pytest.fixture
def typology(app):
    with app.app_context():
        return TypologyTemporistics()


# Додайте ваші тести тут, використовуючи фікстуру typology
def test_typology_temporistics_tetrad(typology):
    # Проверим корректное описание тетрады
    description = typology.get_tetrad_description("6-1-2")
    assert "Era of Individuality" in description

def test_typology_temporistics_invalid_tetrad(typology):
    import pytest
    with pytest.raises(ValueError):
        typology.get_tetrad_description("invalid")

def test_typology_temporistics_quadra(typology):
    types = typology.get_quadra_types("Antipodes")
    assert "Game Master" in types

def test_typology_temporistics_invalid_quadra(typology):
    import pytest
    with pytest.raises(ValueError):
        typology.get_quadra_types("NonExistentQuadra")
