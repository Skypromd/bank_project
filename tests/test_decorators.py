import logging
import sys
from unittest.mock import patch

import pytest

from src.decorators import log


# Пример функции для тестирования
@log()
def sample_function(x, y):
    return x + y


@log()
def function_with_error(x, y):
    return x / y  # Деление на ноль вызовет ошибку, если y == 0


def test_sample_function_logs_success():
    with patch("logging.info") as mock_logging:
        result = sample_function(3, 5)
        assert result == 8
        mock_logging.assert_called_once_with("sample_function ok")


def test_function_with_error_logs_error():
    with patch("logging.error") as mock_logging:
        with pytest.raises(ZeroDivisionError):
            function_with_error(5, 0)
        mock_logging.assert_called_once()


def test_custom_log_filename():
    with patch("logging.basicConfig") as mock_logging_config:

        @log(filename="test.log")
        def another_sample_function():
            return "done"

        another_sample_function()
        mock_logging_config.assert_called_once_with(
            filename="test.log", level=logging.INFO, format="%(asctime)s - %(message)s"
        )


def test_log_no_filename():
    with patch("logging.basicConfig") as mock_logging_config:

        @log()
        def another_function():
            return "done"

        another_function()
        mock_logging_config.assert_called_once_with(
            stream=sys.stdout, level=logging.INFO, format="%(asctime)s - %(message)s"
        )


if __name__ == "__main__":
    pytest.main()
