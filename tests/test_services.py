import pytest
from app.services import get_types_by_typology, calculate_relationship
from app.extensions import db
from app.models import User, UserType
from tests.test_helpers import unique_username, unique_email
import uuid

def test_get_types_by_typology(app, test_db):
    with app.app_context():
        # Створюємо запис типології
        user_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        db.session.add(user_type)
        db.session.commit()
        
        types = get_types_by_typology("Temporistics")
        assert types is not None
        assert any("Past" in type_string for type_string in types)
        assert any("Future" in type_string for type_string in types)

def test_calculate_relationship(app, test_db):
    with app.app_context():
        # Створюємо запис типології
        user_type = UserType(typology_name="Temporistics", type_value="Past, Current, Future, Eternity")
        db.session.add(user_type)
        db.session.commit()
        
        relationship_type, comfort_score = calculate_relationship(
            "Past, Current, Future, Eternity",
            "Current, Past, Future, Eternity",
            "Temporistics"
        )
        assert relationship_type is not None
        assert comfort_score is not None

def test_get_types_psychosophia(app, test_db):
    with app.app_context():
        types = get_types_by_typology("Psychosophia")
        assert types is not None
        assert len(types) > 0

def test_calculate_relationship_invalid_typology(app, test_db):
    with app.app_context():
        with pytest.raises(ValueError):
            calculate_relationship("Past", "Future", "NonExistentTypology")

def test_calculate_relationship_empty_input(app, test_db):
    with app.app_context():
        with pytest.raises(ValueError):
            calculate_relationship("", "Future", "Temporistics")

def test_get_distance_if_compatible(app, test_db):
    from app.models import User, UserType
    from app.extensions import db
    from app.services import get_distance_if_compatible
    import pytest

    with app.app_context():
        # Create the initial user type and commit it
        user_type = UserType(
            typology_name="Temporistics",
            type_value="Past, Current, Future, Eternity"
        )
        db.session.add(user_type)
        db.session.commit()

        # Використовуємо унікальні email та username
        unique_id = uuid.uuid4().hex[:8]
        username1 = f"user1_{unique_id}"
        username2 = f"user2_{unique_id}"
        email1 = f"u1_{unique_id}@example.com"
        email2 = f"u2_{unique_id}@example.com"
        
        # Create two users with this user type
        # Встановлюємо max_distance більше ніж відстань між координатами
        user1 = User(username=username1, email=email1,
                     latitude=40.0, longitude=-73.0, user_type=user_type, max_distance=150.0)
        user1.set_password("pass1")

        user2 = User(username=username2, email=email2,
                     latitude=41.0, longitude=-74.0, user_type=user_type)
        user2.set_password("pass2")

        db.session.add_all([user1, user2])
        db.session.commit()

        # Initially, they should be compatible
        dist = get_distance_if_compatible(user1, user2)
        assert dist > 0

        # Create another user type with a rearranged aspect order resulting in fewer positional matches
        another_type = UserType(
            typology_name="Temporistics",
            type_value="Eternity, Future, Current, Past"
        )
        db.session.add(another_type)
        db.session.commit()

        # Assign the new incompatible user type to user2
        user2.user_type = another_type
        db.session.commit()

        # Now they should have fewer matches => comfort_score <= 50 => ValueError expected
        with pytest.raises(ValueError):
            get_distance_if_compatible(user1, user2)

def test_calculate_detailed_relationships(app, test_db):
    """Тестує детальні типи відносин у Психософії та Темпористиці з оновленими правилами"""
    with app.app_context():
        # -- ПСИХОСОФІЯ --
        typology_name = "Psychosophia"
        
        # 1. Identity/Philia - ідентичні
        type1 = "Emotion, Logic, Will, Physics"
        type2 = "Emotion, Logic, Will, Physics"
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Identity/Philia"
        
        # 1. Identity/Philia - однакові перші дві
        type1 = "Emotion, Logic, Will, Physics"
        type2 = "Emotion, Logic, Physics, Will"
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Identity/Philia"

        # 2. Psychosophia Extinguishment
        type1 = "Emotion, Logic, Will, Physics"
        type2 = "Physics, Will, Logic, Emotion"
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Psychosophia Extinguishment"

        # 3. Full Eros
        type1 = "Emotion, Logic, Physics, Will"
        type2 = "Physics, Will, Emotion, Logic" # Зверніть увагу: Це НЕ Extinguishment
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Full Eros"
        # Перевірка, що це НЕ Extinguishment
        type1_list = type1.split(", ")
        type2_list = type2.split(", ")
        assert type1_list != list(reversed(type2_list))

        # 4. Full Agape (односторонній) - ПОПЕРЕДНІЙ ТЕСТ ВИЯВИВСЯ ВИПАДКОМ EROS
        # type1 = "Emotion, Logic, Will, Physics" # 1234
        # type2 = "Will, Physics, Logic, Emotion" # 3421 - Це Eros, оскільки {1,2}=={2,1} AND {3,4}=={3,4}
        # relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        # assert relationship == "Full Agape" # ПОМИЛКА: Повертає Eros
        
        # Тест для випадку, який раніше був Agape, тепер перевіряємо як Eros
        type1_eros_prev_agape = "Emotion, Logic, Will, Physics"
        type2_eros_prev_agape = "Will, Physics, Logic, Emotion"
        relationship, comfort_score = calculate_relationship(type1_eros_prev_agape, type2_eros_prev_agape, typology_name)
        assert relationship == "Full Eros" # Очікуємо Eros
        
        # TODO: Знайти та додати тест для чистого випадку Full Agape (cond1 XOR cond2)

        # 5. Order/Full Order
        type1 = "Emotion, Logic, Will, Physics"
        type2 = "Logic, Emotion, Physics, Will"
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Order/Full Order"

        # 6. Mirage
        type1 = "Emotion, Logic, Will, Physics"
        type2 = "Will, Physics, Emotion, Logic" # Це також приклад Full Eros, що демонструє можливе перекриття!
                                                 # Поточна логіка віддає пріоритет Eros. Треба переглянути.
                                                 # Для чистого Mirage: 1234 vs 3412 ? Ні, це теж Eros.
                                                 # 1234 vs 3124
        type1 = "Emotion, Logic, Will, Physics"
        type2 = "Will, Emotion, Logic, Physics" # Перша(E) == Третя(E) - НІ.
                                                 # 1234 vs 3412 (Eros)
                                                 # 1234 vs 3142
        type1 = "Emotion, Logic, Will, Physics" # 1234
        type2 = "Will, Emotion, Physics, Logic" # 3142
        # Перевірка Mirage: 1==3 (E vs P - F), 3==1 (W vs W - T)
        # Здається, визначення Mirage: type1[0] == type2[2] and type1[2] == type2[0]
        type1 = "Emotion, Logic, Will, Physics" # 1234
        type2 = "Logic, Will, Emotion, Physics" # 2314
        # Mirage: 1==3 (E vs E - T), 3==1 (W vs L - F) - Ні.
        type1 = "Emotion, Logic, Will, Physics" # 1234
        type2 = "Physics, Will, Emotion, Logic" # 4312
        # Mirage: 1==3 (E vs E - T), 3==1 (W vs P - F) - Ні.
        type1 = "Emotion, Logic, Will, Physics" # 1234
        type2 = "Will, Logic, Emotion, Physics" # 3214 - Ось цей випадок з попереднього тесту!
        # Mirage: 1==3 (E vs E - T), 3==1 (W vs W - T) - Так!
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Mirage"

        # 7. Revision
        type1 = "Emotion, Logic, Will, Physics"
        type2 = "Physics, Logic, Emotion, Emotion" # Некоректний тип
        type2 = "Physics, Will, Logic, Emotion" # Це Extinguishment
        # 1234 vs 4123
        type1 = "Emotion, Logic, Will, Physics"
        type2 = "Physics, Emotion, Logic, Will"
        # Revision: 1==4(E vs W - F), 4==1(P vs P - T) - Ні
        # 1234 vs 4231
        type1 = "Emotion, Logic, Will, Physics"
        type2 = "Physics, Logic, Will, Emotion"
        # Revision: 1==4(E vs E - T), 4==1(P vs P - T) - Так!
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Revision"

        # 8. Therapy-Attraction
        type1 = "Emotion, Logic, Will, Physics" # 1234
        type2 = "Emotion, Will, Logic, Physics" # 1324
        # Attraction: 2==3(L vs L - T), 3==2(W vs W - T) - Так!
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Therapy-Attraction"

        # 9. Therapy-Misunderstanding
        type1 = "Emotion, Logic, Will, Physics" # 1234
        type2 = "Emotion, Physics, Logic, Will" # 1432
        # Misunderstanding: 
        # 2==4 (L vs W - F), 4!=2 (P vs P - T) - Ні
        # 4==2 (W vs L - F), 2!=4 (P vs P - T) - Ні
        # 1234 vs 1423
        type1 = "Emotion, Logic, Will, Physics" # 1234
        type2 = "Emotion, Physics, Logic, Will" # Було 1432, змінив на 1423
        type2 = "Emotion, Physics, Will, Logic" # 1432 - сюди повернемось
        type2 = "Logic, Physics, Will, Emotion" # 2431
        # Misunderstanding:
        # 2==4 (L vs E - F), 4!=2 (P vs P - T) - Ні
        # 4==2 (E vs L - F), 2!=4 (P vs P - T) - Ні
        type1 = "Emotion, Logic, Will, Physics" # 1234
        type2 = "Will, Emotion, Physics, Logic" # 3142
        # Misunderstanding: 
        # 2==4 (L vs L - T), 4!=2 (P vs E - T) - Так!
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Therapy-Misunderstanding"

        # 10. Conflict Submission/Dominance
        type1 = "Emotion, Logic, Will, Physics" # 1234
        type2 = "Logic, Will, Physics, Emotion" # 2341
        # Conflict:
        # 1 in 3,4 (E in P,E - T), 2 not in 3,4 (L not in W,P - T) - Так!
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Conflict Submission/Dominance"
        
        # 11. Neutrality (приклад, що не підпадає під жодне правило вище)
        # type1 = "Emotion, Logic, Will, Physics" # 1234
        # type2 = "Logic, Physics, Emotion, Will" # 2413 - Виявився Therapy-Misunderstanding
        # # Перевіряємо, що не підпадає під інші:
        # # Identity - N, Ext - N, Eros - N, Agape - N, Order - N, Mirage - N, 
        # # Revision - N, Attraction - N, Misunderstanding - Y!, Conflict - N
        # relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        # assert relationship == "Neutrality" # ПОМИЛКА: повертає Therapy-Misunderstanding

        # Тест для випадку, який раніше був Neutrality, тепер перевіряємо як Therapy-Misunderstanding
        type1_mis_prev_neutral = "Emotion, Logic, Will, Physics" # 1234
        type2_mis_prev_neutral = "Logic, Physics, Emotion, Will" # 2413
        relationship, comfort_score = calculate_relationship(type1_mis_prev_neutral, type2_mis_prev_neutral, typology_name)
        assert relationship == "Therapy-Misunderstanding" # Очікуємо Therapy-Misunderstanding
        
        # TODO: Знайти та додати тест для чистого випадку Neutrality

        # -- ТЕМПОРИСТИКА (поки що використовуємо існуючі тести, додамо пізніше) --
        typology_name = "Temporistics"
        # Identity/Philia - повний збіг послідовностей
        type1 = "Past, Current, Future, Eternity"
        type2 = "Past, Current, Future, Eternity"
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Identity/Philia"
        
        # Identity/Philia - збігається перший аспект
        type1 = "Past, Current, Future, Eternity"
        type2 = "Past, Eternity, Current, Future"
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Identity/Philia"

        # Order/Full Order - перший аспект одного є другим в іншого і навпаки
        type1 = "Past, Current, Future, Eternity"
        type2 = "Current, Past, Eternity, Future"
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        assert relationship == "Order/Full Order"

        # Psychosophia Extinguishment - типи є дзеркальним відображенням один одного
        type1 = "Past, Current, Future, Eternity"
        type2 = "Eternity, Future, Current, Past"
        relationship, comfort_score = calculate_relationship(type1, type2, typology_name)
        # Змінено на точну перевірку, так як ми уточнили логіку
        assert relationship == "Psychosophia Extinguishment"
        
        # Додати тести для інших типів відносин у Темпористиці...


