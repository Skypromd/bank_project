# tests/test_generators.py
from typing import Dict, List

import pytest
from decorators import log

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions() -> List[Dict]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]


def test_filter_by_currency(transactions: List[Dict]) -> None:
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 2

    rub_transactions = list(filter_by_currency(transactions, "RUB"))
    assert len(rub_transactions) == 0


def test_transaction_descriptions(transactions: List[Dict]) -> None:
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == ["Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет"]


def test_card_number_generator() -> None:
    generator = card_number_generator(1, 5)
    numbers = list(generator)
    assert numbers == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]


# Эти функции могут быть использованы для тестирования
@log()
def add(x: int, y: int) -> int:
    return x + y


@log()
def divide(x: int, y: int) -> float:
    return x / y


def test_add(capsys: pytest.CaptureFixture) -> None:
    add(1, 2)
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_divide(capsys: pytest.CaptureFixture) -> None:
    result = divide(4, 2)
    assert result == 2.0
    captured = capsys.readouterr()
    assert "divide ok" in captured.out


def test_divide_by_zero(capsys: pytest.CaptureFixture) -> None:
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
    captured = capsys.readouterr()
    assert "divide error: division by zero" in captured.out
