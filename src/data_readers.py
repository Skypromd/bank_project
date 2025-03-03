"""Модуль для чтения финансовых транзакций из CSV и Excel файлов."""
import pandas as pd
from typing import List, Dict, Any



def read_csv_transactions(path: str) -> List[Dict[str, Any]]:
    """Читает финансовые транзакции из CSV-файла.

    Args:
        path (str): Путь к CSV-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями.

    Raises:
        ValueError: Если файл не найден или пуст.
    """
    try:
        df = pd.read_csv(path)
        return df.to_dict("records")
    except FileNotFoundError:
        raise ValueError(f"Файл {path} не найден")
    except pd.errors.EmptyDataError:
        return []


def read_excel_transactions(path: str) -> List[Dict[str, Any]]:
    """Читает финансовые транзакции из Excel-файла.

    Args:
        path (str): Путь к Excel-файлу.

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями.

    Raises:
        ValueError: Если файл не найден или пуст.
    """
    try:
        df = pd.read_excel(path)
        return df.to_dict("records")
    except FileNotFoundError:
        raise ValueError(f"Файл {path} не найден")
    except pd.errors.EmptyDataError:
        return []