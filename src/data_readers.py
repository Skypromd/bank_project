# src/data_readers.py
from typing import List, Dict, Any
import pandas as pd

def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает транзакции из CSV-файла.

    Args:
        file_path: Путь к CSV-файлу.

    Returns:
        Список словарей с данными транзакций.

    Raises:
        ValueError: Если файл не найден.
    """
    try:
        df = pd.read_csv(file_path)
        transactions = [{str(k): v for k, v in record.items()} for record in df.to_dict(orient="records")]
        return transactions
    except FileNotFoundError:
        raise ValueError(f"Файл {file_path} не найден")
    except pd.errors.EmptyDataError:
        return []

def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает транзакции из Excel-файла.

    Args:
        file_path: Путь к Excel-файлу.

    Returns:
        Список словарей с данными транзакций.

    Raises:
        ValueError: Если файл не найден.
    """
    try:
        df = pd.read_excel(file_path)
        transactions = [{str(k): v for k, v in record.items()} for record in df.to_dict(orient="records")]
        return transactions
    except FileNotFoundError:
        raise ValueError(f"Файл {file_path} не найден")
    except pd.errors.EmptyDataError:
        return []