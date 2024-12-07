import pytest
from app.services import get_types_by_typology, calculate_relationship


def test_get_types_by_typology(app):
    with app.app_context():
        types = get_types_by_typology("Temporistics")
        assert types is not None
        assert any("Past" in type_string for type_string in types)
        assert any("Future" in type_string for type_string in types)


def test_calculate_relationship(app):
    with app.app_context():
        relationship_type, comfort_score = calculate_relationship(
            "Past", "Future", "Temporistics"
        )
        assert relationship_type is not None
        assert comfort_score is not None


def test_get_types_psychosophia(app):
    with app.app_context():
        types = get_types_by_typology("Psychosophia")
        assert types is not None
        assert len(types) > 0  # Проверим, что не пусто

def test_calculate_relationship_invalid_typology(app):
    with app.app_context():
        with pytest.raises(ValueError):
            calculate_relationship("Past", "Future", "NonExistentTypology")


def test_calculate_relationship_empty_input(app):
    with app.app_context():
        with pytest.raises(ValueError):
            calculate_relationship("", "Future", "Temporistics")
