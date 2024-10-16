import pytest
from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    # Проверка корректного маскирования
    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"
    assert get_mask_card_number(1234567812345678) == "1234 56** **** 5678"

    # Проверка на короткие номера
    with pytest.raises(ValueError):
        get_mask_card_number(123456)

    # Проверка на отрицательное значение
    with pytest.raises(ValueError):
        get_mask_card_number(-7000792289606361)


def test_get_mask_account() -> None:
    # Проверка корректного маскирования
    assert get_mask_account(73654108430135874305) == "**4305"
    assert get_mask_account(12345678901234567890) == "**7890"

    # Проверка на короткие номера
    with pytest.raises(ValueError):
        get_mask_account(123)

    # Проверка на отрицательное значение
    with pytest.raises(ValueError):
        get_mask_account(-73654108430135874305)
