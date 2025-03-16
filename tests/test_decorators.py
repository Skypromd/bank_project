# tests/test_decorators.py
import logging
from unittest.mock import patch

import pytest

from src.decorators import log


class TestDecorators:
    def test_log_without_filename_success(self):
        """Проверка успешного логирования без указания имени файла."""

        @log()
        def my_function(x, y):
            return x + y

        with patch("logging.Logger.info") as mock_logging_info:
            result = my_function(3, 5)
            assert result == 8
            assert (
                mock_logging_info.call_count == 2
            )  # Ожидаем два вызова (успех и время)

    def test_log_with_filename_success(self):
        """Проверка успешного логирования с указанием имени файла."""

        @log("test_log.txt")
        def my_function(x, y):
            return x + y

        with patch("logging.FileHandler") as mock_file_handler:
            mock_file_handler.return_value.level = (
                logging.INFO
            )  # Устанавливаем уровень для мока
            with patch("logging.Logger.info") as mock_logging_info:
                result = my_function(3, 5)
                assert result == 8
                mock_file_handler.assert_called_once_with("test_log.txt")
                assert mock_logging_info.call_count == 2  # Ожидаем два вызова

    def test_log_with_error(self):
        """Проверка логирования при возникновении ошибки."""

        @log("test_log.txt")
        def my_function(_x, _y):
            raise ValueError("Test error")

        with patch("logging.FileHandler") as mock_file_handler:
            mock_file_handler.return_value.level = (
                logging.ERROR
            )  # Устанавливаем уровень для мока
            with patch("logging.Logger.error") as mock_logging_error:
                with pytest.raises(ValueError):
                    my_function(3, 5)
                mock_file_handler.assert_called_once_with("test_log.txt")
                assert mock_logging_error.call_count == 1  # Проверяем вызов error

    def test_log_with_none_filename(self):
        """Проверка логирования с None как filename."""

        @log(None)
        def my_function(x, y):
            return x + y

        with patch("logging.StreamHandler") as mock_stream_handler:
            mock_stream_handler.return_value.level = (
                logging.INFO
            )  # Устанавливаем уровень для мока
            with patch("logging.Logger.info") as mock_logging_info:
                result = my_function(3, 5)
                assert result == 8
                mock_stream_handler.assert_called_once()
                assert mock_logging_info.call_count == 2  # Ожидаем два вызова
