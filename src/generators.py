# src/generators.py

import functools
import logging
import sys
from typing import Any, Callable, Dict, Iterator, List, Optional


def filter_by_currency(transactions: List[Dict], currency: str) -> Iterator[Dict]:
    """Возвращает итератор транзакций по заданной валюте."""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """Генератор, возвращающий описания транзакций по очереди."""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генератор для генерации номеров карт в заданном диапазоне."""
    for number in range(start, stop + 1):
        yield f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " + f"{number:016d}"[
            8:12
        ] + " " + f"{number:016d}"[12:16]


def log(filename: Optional[str] = None) -> Callable:
    # Настройка логирования
    logging.basicConfig(
        filename=filename,
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        stream=sys.stdout if filename is None else None,
    )

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                logging.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                logging.error(f"{func.__name__} error: {str(e)}. Inputs: {args}, {kwargs}")
                raise

        return wrapper

    return decorator
