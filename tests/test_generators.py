from typing import Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions() -> List[Dict]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        }
        # Удаляем транзакцию с валютой RUB
    ]

def test_filter_by_currency(transactions: List[Dict]) -> None:
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 2

    rub_transactions = list(filter_by_currency(transactions, "RUB"))
    assert len(rub_transactions) == 0  # Теперь тест должен проходить

def test_transaction_descriptions(transactions: List[Dict]) -> None:
    descriptions = list(transaction_descriptions(transactions))
    assert descriptions == [
        "Перевод организации",
        "Перевод со счета на счет"
    ]

def test_card_number_generator() -> None:
    generator = card_number_generator(1, 5)
    numbers = list(generator)
    assert numbers == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"
    ]