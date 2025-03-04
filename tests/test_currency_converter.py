import unittest
from unittest.mock import patch, Mock

import requests
# Предполагаем, что это ваш модуль с функцией convert_currency
from currency_converter import convert_currency  # Замените на правильный импорт


class TestConvertCurrency(unittest.TestCase):

    @patch("currency_converter.requests.get")  # Мокаем requests.get
    def test_convert_currency_success(self, mock_get):
        """Тесты успешной конвертации валют."""
        # Настраиваем мок для API
        mock_response = Mock()
        mock_response.json.return_value = {"info": {"rate": 75.0}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Тест 1: Конвертация USD в RUB
        transaction_usd = {"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}
        result_usd = convert_currency(transaction_usd)
        self.assertEqual(result_usd, 7500.0, "Ошибка конвертации USD в RUB")

        # Тест 2: Обработка RUB без конвертации
        transaction_rub = {"operationAmount": {"amount": "31957.58", "currency": {"code": "RUB"}}}
        result_rub = convert_currency(transaction_rub)
        self.assertEqual(result_rub, 31957.58, "Ошибка обработки RUB")

    @patch("currency_converter.requests.get")
    def test_convert_currency_unsupported_currency(self, mock_get):
        """Тест обработки неподдерживаемой валюты."""
        transaction_invalid = {"operationAmount": {"amount": "100.00", "currency": {"code": "JPY"}}}
        result_invalid = convert_currency(transaction_invalid)
        self.assertEqual(result_invalid, 0.0, "Неподдерживаемая валюта должна возвращать 0.0")

    @patch("currency_converter.requests.get")
    def test_convert_currency_api_error(self, mock_get):
        """Тест обработки ошибок API."""
        mock_get.side_effect = requests.RequestException("Ошибка API")
        transaction_api_error = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}
        result_api_error = convert_currency(transaction_api_error)
        self.assertEqual(result_api_error, 0.0, "Ошибка API должна возвращать 0.0")

    def test_convert_currency_missing_fields(self):
        """Тесты для случаев с отсутствующими или некорректными полями."""
        # Тест 1: Отсутствует operationAmount
        transaction_missing_operation = {}
        result_missing_operation = convert_currency(transaction_missing_operation)
        self.assertEqual(result_missing_operation, 0.0, "Отсутствие operationAmount должно возвращать 0.0")

        # Тест 2: Отсутствует amount
        transaction_missing_amount = {"operationAmount": {"currency": {"code": "USD"}}}
        result_missing_amount = convert_currency(transaction_missing_amount)
        self.assertEqual(result_missing_amount, 0.0, "Отсутствие amount должно возвращать 0.0")

        # Тест 3: Отрицательная сумма
        transaction_negative_amount = {"operationAmount": {"amount": "-100.00", "currency": {"code": "USD"}}}
        result_negative_amount = convert_currency(transaction_negative_amount)
        self.assertEqual(result_negative_amount, 0.0, "Отрицательная сумма должна возвращать 0.0")

        # Тест 4: Некорректный формат amount
        transaction_invalid_amount = {"operationAmount": {"amount": "abc", "currency": {"code": "USD"}}}
        result_invalid_amount = convert_currency(transaction_invalid_amount)
        self.assertEqual(result_invalid_amount, 0.0, "Некорректный amount должен возвращать 0.0")

    @patch("currency_converter.logging.info")
    def test_logging(self, mock_logging):
        """Тест логирования успешной конвертации."""
        with patch("currency_converter.get_conversion_rate", return_value=80.0):
            transaction = {"operationAmount": {"amount": "50", "currency": {"code": "USD"}}}
            convert_currency(transaction)
            mock_logging.assert_called_with("Конвертировано 50 USD в 4000.00 RUB")


if __name__ == "__main__":
    unittest.main()