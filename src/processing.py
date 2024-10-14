from typing import Dict, List


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Фильтрует список словарей по значению ключа 'state'.

    Args:
        transactions (List[Dict]): Список словарей с данными о банковских операциях.
        state (str, optional): Значение для фильтрации по ключу 'state'. По умолчанию 'EXECUTED'.

    Returns:
        List[Dict]: Новый список словарей, соответствующих условию фильтрации.
    """
    return [transaction for transaction in transactions if transaction.get("state") == state]


def sort_by_date(transactions: List[Dict], descending: bool = True) -> List[Dict]:
    """Сортирует список словарей по дате.

    Args:
        transactions (List[Dict]): Список словарей с данными о банковских операциях.
        descending (bool, optional): Указывает порядок сортировки. По умолчанию True (по убыванию).

    Returns:
        List[Dict]: Новый список словарей, отсортированных по дате.
    """
    return sorted(transactions, key=lambda x: x["date"], reverse=descending)
