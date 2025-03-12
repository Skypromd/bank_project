# src/processing.py
from typing import List, Dict


def filter_by_state(transactions: List[Dict], state: str) -> List[Dict]:
    """Фильтрует транзакции по заданному статусу.

    Args:
        transactions: Список транзакций.
        state: Статус для фильтрации (например, 'EXECUTED', 'CANCELED', 'PENDING').

    Returns:
        Отфильтрованный список транзакций.
    """
    return [t for t in transactions if t.get("state") == state]


def sort_by_date(transactions: List[Dict], descending: bool = False) -> List[Dict]:
    """Сортирует транзакции по дате.

    Args:
        transactions: Список транзакций.
        descending: True для сортировки по убыванию, False для возрастания.

    Returns:
        Отсортированный список транзакций.
    """
    return sorted(transactions, key=lambda x: x.get("date", ""), reverse=descending)


def search_transactions_by_description(transactions: List[Dict], search_str: str) -> List[Dict]:
    """Ищет транзакции по подстроке в описании.

    Args:
        transactions: Список транзакций.
        search_str: Подстрока для поиска в описании.

    Returns:
        Список транзакций, где описание содержит заданную подстроку.
    """
    return [t for t in transactions if search_str.lower() in t.get("description", "").lower()]


def filter_by_currency(transactions: List[Dict], currency: str) -> List[Dict]:
    """Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список транзакций.
        currency: Код валюты для фильтрации (например, 'RUB', 'USD').

    Returns:
        Отфильтрованный список транзакций.
    """
    return [
        t
        for t in transactions
        if t.get("operationAmount", {}).get("currency", {}).get("code", "") == currency
        or t.get("currency", {}).get("code", "") == currency
    ]
