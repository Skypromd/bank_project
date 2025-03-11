# tests/test_widget.py
import sys
import os
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.widget import get_date, mask_account_card

def test_mask_account_card():
    test_cases = [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Visa1234567890123456", "Visa 1234 56** **** 3456")
    ]
    for input_str, expected in test_cases:
        assert mask_account_card(input_str) == expected

def test_mask_account_card_invalid():
    """Тест обработки некорректного ввода."""
    assert mask_account_card("Visa 123") == "Invalid input format"

def test_mask_account_card_short_card_number():
    """Тест обработки короткого номера карты."""
    assert mask_account_card("Visa 12345") == "Invalid input format"

def test_mask_account_card_no_space_short():
    assert mask_account_card("Visa123") == "Invalid input format"

def test_get_date():
    test_cases = [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2019-07-03T18:35:29.512364", "03.07.2019")
    ]
    for input_date, expected in test_cases:
        assert get_date(input_date) == expected