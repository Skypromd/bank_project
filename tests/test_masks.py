import pytest

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date


def test_get_mask_card_number() -> None:


    """Тестирование функции get_mask_card_number."""

    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"
    with pytest.raises(ValueError):
        get_mask_card_number(123456)


def test_get_mask_account() -> None:

    """Тестирование функции get_mask_account."""

    assert get_mask_account(73654108430135874305) == "**4305"
    with pytest.raises(ValueError):
        get_mask_account(123)


def test_filter_by_state() -> None:
    """Тестирование функции filter_by_state."""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-02"},
    ]
    result = filter_by_state(transactions)
    assert len(result) == 1
    assert result[0]["state"] == "EXECUTED"


def test_sort_by_date() -> None:
    """Тестирование функции sort_by_date."""
    transactions = [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-02"},
    ]
    result = sort_by_date(transactions)
    assert result[0]["id"] == 2  # Проверка, что id 2 идёт первой при сортировке
