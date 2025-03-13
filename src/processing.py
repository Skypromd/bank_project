# src/processing.py
from typing import List, Dict
import re
from collections import Counter

def filter_by_state(transactions: List[Dict], state: str) -> List[Dict]:
    """Фильтрует транзакции по заданному статусу."""
    return [t for t in transactions if t.get("state") == state]

def sort_by_date(transactions: List[Dict], descending: bool = False) -> List[Dict]:
    """Сортирует транзакции по дате."""
    return sorted(transactions, key=lambda x: x.get("date", ""), reverse=descending)

def search_transactions_by_description(transactions: List[Dict], search_str: str) -> List[Dict]:
    """Ищет транзакции по подстроке в описании с использованием регулярных выражений.

    Args:
        transactions: Список транзакций.
        search_str: Строка или регулярное выражение для поиска.

    Returns:
        Список транзакций, где описание соответствует поиску.
    """
    pattern = re.compile(search_str, re.IGNORECASE)
    return [t for t in transactions if pattern.search(t.get("description", ""))]

def filter_by_currency(transactions: List[Dict], currency: str) -> List[Dict]:
    """Фильтрует транзакции по заданной валюте."""
    return [t for t in transactions if t.get("operationAmount", {}).get("currency", {}).get("code", "") == currency or t.get("currency", {}).get("code", "") == currency]

def count_transactions_by_category(transactions: List[Dict]) -> Dict[str, int]:
    """Подсчитывает количество операций по категориям с использованием Counter.

    Args:
        transactions: Список транзакций.

    Returns:
        Словарь с категориями (описаниями) и количеством операций.
    """
    descriptions = [t.get("description", "Unknown") for t in transactions]
    return dict(Counter(descriptions))