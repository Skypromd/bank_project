from typing import List, Dict, Optional

def filter_by_state(transactions: List[Dict], state: Optional[str] = 'EXECUTED') -> List[Dict]:
    """
    Фильтрует список словарей по состоянию.

    :param transactions: Список словарей с данными о банковских операциях.
    :param state: Значение для ключа 'state' (по умолчанию 'EXECUTED').
    :return: Новый список словарей с соответствующим состоянием.
    """
    return [transaction for transaction in transactions if transaction.get('state') == state]


from datetime import datetime

def sort_by_date(transactions: List[Dict], descending: Optional[bool] = True) -> List[Dict]:
    """
    Сортирует список словарей по дате.

    :param transactions: Список словарей с данными о банковских операциях.
    :param descending: Параметр, задающий порядок сортировки (по умолчанию True).
    :return: Новый отсортированный список словарей.
    """
    return sorted(transactions, key=lambda x: datetime.fromisoformat(x['date']), reverse=descending)