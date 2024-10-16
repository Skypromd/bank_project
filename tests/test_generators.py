import pytest
import logging
from src.decorators import log
from src.generators import filter_by_currency

# Включение логирования для тестов
logging.basicConfig(level=logging.INFO)


@log()
def successful_function(x, y):
    return x + y


@log()
def error_function(x, y):
    return x / y


def test_logging_success(caplog):
    with caplog.at_level(logging.INFO):  # Захватываем логи на уровне INFO
        result = successful_function(1, 2)
        assert result == 3

    assert "successful_function ok" in caplog.text  # Проверяем, что сообщение в логах


def test_logging_error(caplog):
    with caplog.at_level(logging.ERROR):  # Захватываем логи на уровне ERROR
        with pytest.raises(ZeroDivisionError):
            error_function(1, 0)

    assert "error_function error: ZeroDivisionError" in caplog.text  # Проверяем, что сообщение в логах


def test_filter_by_currency():
    transactions = [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "USD Transaction"},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}, "description": "EUR Transaction"},
        {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}, "description": "RUB Transaction"},
    ]

    usd_transactions = filter_by_currency(transactions, "USD")
    assert len(usd_transactions) == 1
    assert usd_transactions[0]["operationAmount"]["currency"]["code"] == "USD"

    rub_transactions = filter_by_currency(transactions, "RUB")
    assert len(rub_transactions) == 1
    assert rub_transactions[0]["operationAmount"]["currency"]["code"] == "RUB"

    jpy_transactions = filter_by_currency(transactions, "JPY")
    assert len(jpy_transactions) == 0  # Ожидается 0 транзакций в JPY
