# tests/test_widget.py
from src.widget import get_date, mask_account_card


def test_mask_account_card():
    """Тест маскировки карты."""
    assert mask_account_card("Visa 1234567890123456") == "Visa 123456 78** **** 3456"


def test_mask_account_card_invalid():
    """Тест обработки некорректного номера карты."""
    assert mask_account_card("Visa 123") == "Неверный формат номера карты"


def test_mask_account_card_empty():
    """Тест обработки пустого входного значения."""
    assert mask_account_card("") == "Неверный формат номера карты"


def test_mask_account_card_short_card_number():
    """Тест обработки короткого номера карты."""
    assert mask_account_card("Visa 1234567890") == "Visa 1234** 7890"


def test_mask_account_card_no_space_short():
    """Тест обработки номера карты без пробела и короткого."""
    assert mask_account_card("1234567890") == "1234** 7890"


def test_mask_account_card_short_boundary():
    """Тест обработки номера карты на границе длины (4 и 5 символов)."""
    assert mask_account_card("Visa 1234") == "Неверный формат номера карты"
    assert mask_account_card("Visa 12345") == "Visa 1234** 2345"


def test_get_date():
    """Тест форматирования даты."""
    assert get_date("2023-01-01T12:00:00") == "2023-01-01"
    assert get_date("invalid_date") == "N/A"
    assert get_date("") == "N/A"
