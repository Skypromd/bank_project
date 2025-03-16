# src/processing.py
from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(
    transactions: List[Dict[str, Any]], state: str
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.

    :param transactions: Список транзакций.
    :param state: Статус для фильтрации (EXECUTED, CANCELED, PENDING).
    :return: Список отфильтрованных транзакций.
    """
    return [t for t in transactions if t.get("state") == state]


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency: str
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте.

    :param transactions: Список транзакций.
    :param currency: Код валюты для фильтрации (например, "RUB").
    :return: Список отфильтрованных транзакций.
    """
    return [
        t
        for t in transactions
        if (
            (
                isinstance(t.get("operationAmount", {}).get("currency", {}), dict)
                and t.get("operationAmount", {}).get("currency", {}).get("code", "")
                == currency
            )
            or t.get("currency", "") == currency
            or (
                isinstance(t.get("operationAmount", {}).get("currency", ""), str)
                and t.get("operationAmount", {}).get("currency", "") == currency
            )
        )
    ]


def sort_by_date(
    transactions: List[Dict[str, Any]], reverse: bool = False
) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    :param transactions: Список транзакций.
    :param reverse: Если True, сортировка по убыванию, иначе по возрастанию.
    :return: Отсортированный список транзакций.
    """

    def parse_date(t: Dict[str, Any]) -> datetime:
        date_str = t.get("date", "1970-01-01T00:00:00")
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            return datetime(1970, 1, 1)

    return sorted(transactions, key=parse_date, reverse=reverse)
