import unittest
from unittest.mock import patch
from src.external_api.currency_converter import convert_currency

class TestConvertCurrency(unittest.TestCase):

    @patch("src.external_api.currency_converter.requests.get")
    def test_convert_currency_valid_usd(self, mock_get):
        mock_get.return_value.json.return_value = {"result": 100.0}
        transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}
        result = convert_currency(transaction)
        self.assertEqual(result, 100.0)

    @patch("src.external_api.currency_converter.requests.get")
    def test_convert_currency_valid_rub(self, mock_get):
        mock_get.return_value.json.return_value = {"result": 31957.58}
        transaction = {"operationAmount": {"amount": "31957.58", "currency": {"code": "RUB"}}}
        result = convert_currency(transaction)
        self.assertEqual(result, 31957.58)

    def test_convert_currency_invalid(self):
        transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "INVALID"}}}
        result = convert_currency(transaction)
        self.assertEqual(result, 0.0)  # Или ожидаемое значение

    def test_convert_currency_missing_operation_amount(self):
        transaction = {}
        result = convert_currency(transaction)
        self.assertEqual(result, 0.0)

if __name__ == "__main__":
    unittest.main()
