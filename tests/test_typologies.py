import pytest
from app.typologies.typology_temporistics import TypologyTemporistics
from app.typologies.typology_psychosophia import TypologyPsychosophia
from app.typologies.typology_amatoric import TypologyAmatoric
from app.typologies.typology_socionics import TypologySocionics


@pytest.fixture
def typology(app):
    with app.app_context():
        return TypologyTemporistics()


# Тесты для Temporistics
def test_typology_temporistics_tetrad(typology):
    description = typology.get_tetrad_description("6-1-2")
    assert "Era of Individuality" in description

def test_typology_temporistics_invalid_tetrad(typology):
    with pytest.raises(ValueError):
        typology.get_tetrad_description("invalid")

def test_typology_temporistics_quadra(typology):
    types = typology.get_quadra_types("Antipodes")
    assert "Game Master" in types

def test_typology_temporistics_invalid_quadra(typology):
    with pytest.raises(ValueError):
        typology.get_quadra_types("NonExistentQuadra")

def test_typology_temporistics_relationships(typology):
    # Проверим intertype отношения для Temporistics
    all_types = typology.get_all_types()
    assert len(all_types) > 0
    # Возьмём два одинаковых типа
    same_type = all_types[0]
    relationship_type = typology.determine_relationship_type(same_type, same_type)
    assert relationship_type in ["Complete Unity", "Deep Harmony", "Shared Vision", "Superficial Agreement", "Strategic Conflict", "Unknown Relationship"]

    score, desc = typology.get_comfort_score(relationship_type)
    assert score is not None


# Тесты для Psychosophia
def test_typology_psychosophia_basic():
    typ = TypologyPsychosophia()
    all_types = typ.get_all_types()
    assert len(all_types) > 0
    shortened = typ.shorten_type(all_types[0])
    assert len(shortened[0]) == 4  # Проверим, что сокращение идёт по заглавным буквам аспектов

    # determine_relationship_type
    assert typ.determine_relationship_type(all_types[0], all_types[0]) == "Identity"
    assert typ.determine_relationship_type(all_types[0], "Emotion, Logic, Will, Physics") == "Identity"
    assert typ.determine_relationship_type("BogusType", all_types[0]) == "Unknown Relationship"

    # get_comfort_score
    score, desc = typ.get_comfort_score("Identity")
    assert score == 100
    score, desc = typ.get_comfort_score("Unknown Relationship")
    assert score == 0


# Тесты для Amatoric
def test_typology_amatoric_basic():
    typ = TypologyAmatoric()
    all_types = typ.get_all_types()
    assert len(all_types) > 0, "Amatoric should return some types"
    shortened = typ.shorten_type(all_types[0])
    # Проверим, что сокращение проходит корректно (в Amatoric 4 аспекта: Love, Passion, Friendship, Romance)
    assert len(shortened[0]) == 4

    # determine_relationship_type
    assert typ.determine_relationship_type(all_types[0], all_types[0]) == "Identity"
    assert typ.determine_relationship_type(all_types[0], "Love, Passion, Friendship, Romance") == "Identity"
    # Неизвестный тип
    assert typ.determine_relationship_type("Unknown Type", all_types[0]) == "Unknown Relationship"

    # get_comfort_score
    score, desc = typ.get_comfort_score("Identity")
    assert score == 100
    score, desc = typ.get_comfort_score("Unknown Relationship")
    assert score == 0


# Тесты для Socionics
def test_typology_socionics_basic(app):
    from app.typologies.typology_socionics import TypologySocionics
    with app.test_request_context():
        typ = TypologySocionics()
        all_types = typ.get_all_types()
        assert len(all_types) > 0
        shortened = typ.shorten_type(all_types[0])
        assert len(shortened[0]) > 0

        # determine_relationship_type
        assert typ.determine_relationship_type(all_types[0], all_types[0]) == "Identity"
        assert typ.determine_relationship_type(all_types[0], "BogusType") == "Unknown Relationship"

        # get_comfort_score
        score, desc = typ.get_comfort_score("Identity")
        assert score == 100
        score, desc = typ.get_comfort_score("Unknown Relationship")
        assert score == 0

        # get_dual_type / get_activity_type
        dual = typ.get_dual_type("ILE")
        assert dual == "SEI" or dual is None

        activity = typ.get_activity_type("ILE")
        assert activity == "ESE" or activity is None

        # Проверим quadras в контексте запроса
        quadras = typ.get_all_quadras()
        assert "Alpha" in quadras.keys()
        alpha_types = quadras["Alpha"]["types"]
        assert len(alpha_types) == 4
        # description - переведённая строка, теперь доступна внутри test_request_context
        assert len(quadras["Alpha"]["description"]) > 0
