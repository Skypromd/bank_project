import os
import sys
import unittest

import requests
from unittest.mock import patch

from src.currency_converter import convert_currency, get_conversion_rate

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestConvertCurrency(unittest.TestCase):
    @patch("src.currency_converter.requests.get")
    def test_convert_currency(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"info": {"rate": 75.0}}
        transaction_usd = {"operationAmount": {"amount": "100.0", "currency": {"code": "USD"}}}
        self.assertEqual(convert_currency(transaction_usd), 7500.0)

    @patch("src.currency_converter.requests.get")
    def test_get_conversion_rate(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"info": {"rate": 80.0}}
        self.assertEqual(get_conversion_rate("EUR", "RUB"), 80.0)

    @patch("src.currency_converter.requests.get")
    def test_convert_currency_missing_operation_amount(self, mock_get):
        transaction_empty = {}
        self.assertEqual(convert_currency(transaction_empty), 0.0)
        mock_get.assert_not_called()

    @patch("src.currency_converter.requests.get")
    def test_convert_currency_missing_fields(self, mock_get):
        transaction_missing = {"operationAmount": {"amount": "", "currency": {"code": ""}}}
        self.assertEqual(convert_currency(transaction_missing), 0.0)
        mock_get.assert_not_called()

    @patch("src.currency_converter.requests.get")
    def test_get_conversion_rate_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network error")
        result = get_conversion_rate("USD", "RUB")
        print("RequestException triggered:", result)
        self.assertEqual(result, 0.0)

    @patch("src.currency_converter.requests.get")
    def test_get_conversion_rate_value_error_invalid_rate(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"info": {"rate": "invalid"}}
        self.assertEqual(get_conversion_rate("USD", "RUB"), 0.0)

    @patch("src.currency_converter.requests.get")
    def test_get_conversion_rate_value_error_json(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.side_effect = ValueError("Invalid JSON")
        result = get_conversion_rate("USD", "RUB")
        print("ValueError JSON triggered:", result)
        self.assertEqual(result, 0.0)

    @patch("src.currency_converter.requests.get")
    def test_convert_currency_negative_amount(self, mock_get):
        transaction_negative = {"operationAmount": {"amount": "-100.0", "currency": {"code": "RUB"}}}
        result = convert_currency(transaction_negative)
        print("Negative amount triggered:", result)
        self.assertEqual(result, 0.0)
        self.assertTrue(float("-100.0") < 0)
        mock_get.assert_not_called()

    @patch("src.currency_converter.requests.get")
    def test_convert_currency_rub(self, mock_get):
        transaction_rub = {"operationAmount": {"amount": "500.0", "currency": {"code": "RUB"}}}
        self.assertEqual(convert_currency(transaction_rub), 500.0)
        mock_get.assert_not_called()

    @patch("src.currency_converter.requests.get")
    def test_convert_currency_unsupported_currency(self, mock_get):
        transaction_unsupported = {"operationAmount": {"amount": "100.0", "currency": {"code": "JPY"}}}
        self.assertEqual(convert_currency(transaction_unsupported), 0.0)
        mock_get.assert_not_called()

    @patch("src.currency_converter.requests.get")
    def test_convert_currency_invalid_rate(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"info": {"rate": 0.0}}
        transaction_usd = {"operationAmount": {"amount": "100.0", "currency": {"code": "USD"}}}
        self.assertEqual(convert_currency(transaction_usd), 0.0)

    @patch("src.currency_converter.requests.get")
    def test_get_conversion_rate_with_rates(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"rates": {"RUB": 75.0}}
        result = get_conversion_rate("USD", "RUB")
        print("Rates format triggered:", result)
        self.assertEqual(result, 75.0)

    @patch("src.currency_converter.requests.get")
    def test_get_conversion_rate_invalid_response(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"invalid_key": {}}
        result = get_conversion_rate("EUR", "USD")
        print("Invalid response triggered:", result)
        self.assertEqual(result, 0.0)

    @patch("src.currency_converter.requests.get")
    def test_convert_currency_value_error(self, mock_get):
        transaction_invalid = {"operationAmount": {"amount": "abc", "currency": {"code": "RUB"}}}
        result = convert_currency(transaction_invalid)
        print("ValueError in convert_currency triggered:", result)
        self.assertEqual(result, 0.0)
        mock_get.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
