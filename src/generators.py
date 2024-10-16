import pytest
import logging
from src.decorators import log  # Импортируем декоратор
from typing import Dict, List

# Включение логирования для тестов
logging.basicConfig(level=logging.INFO)


@log()  # Убедитесь, что декоратор правильно применен
def successful_function(x, y):
    return x + y


@log()
def error_function(x, y):
    return x / y


def test_logging_success(capsys):
    result = successful_function(1, 2)
    assert result == 3

    captured = capsys.readouterr()
    assert "successful_function ok" in captured.out


def test_logging_error(capsys):
    with pytest.raises(ZeroDivisionError):
        error_function(1, 0)

    captured = capsys.readouterr()
    assert "error_function error: ZeroDivisionError" in captured.err  # Исправлено на captured.err


@log()
def filter_by_currency(transactions: List[Dict], currency: str) -> List[Dict]:
    """Фильтрует транзакции по заданной валюте.

    Args:
        transactions (List[Dict]): Список транзакций.
        currency (str): Код валюты для фильтрации.

    Returns:
        List[Dict]: Список транзакций, соответствующих указанной валюте.
    """
    return [
        transaction for transaction in transactions if transaction["operationAmount"]["currency"]["code"] == currency
    ]
