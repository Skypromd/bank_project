import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"
    with pytest.raises(ValueError):
        get_mask_card_number(123456)


def test_get_mask_account() -> None:
    assert get_mask_account(73654108430135874305) == "**4305"
    with pytest.raises(ValueError):
        get_mask_account(123)
