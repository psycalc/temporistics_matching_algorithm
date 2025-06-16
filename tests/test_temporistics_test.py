import pytest
from app.temporistics_test import calculate_temporistics_type


def test_calculate_temporistics_type_default_order():
    """Each aspect chosen once should yield the predefined order."""
    answers = ["A", "B", "C", "D"]
    result = calculate_temporistics_type(answers)
    assert result == "Past, Current, Future, Eternity"


def test_calculate_temporistics_type_future_priority():
    """More 'Future' answers should place Future first."""
    answers = ["C", "C", "B", "A"]
    result = calculate_temporistics_type(answers)
    assert result.startswith("Future")
