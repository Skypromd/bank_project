import unittest
from unittest.mock import patch
from src.external_api import convert_currency


class TestExternalAPI(unittest.TestCase):
    @patch("src.external_api.requests.get")
    def test_convert_currency_usd(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": 7500.0}

        transaction = {"amount": 100, "currency": "USD"}
        result = convert_currency(transaction)
        self.assertEqual(result, 7500.0)

    @patch("src.external_api.requests.get")
    def test_convert_currency_eur(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": 8500.0}

        transaction = {"amount": 100, "currency": "EUR"}
        result = convert_currency(transaction)
        self.assertEqual(result, 8500.0)

    @patch("src.external_api.requests.get")
    def test_convert_currency_rub(self, mock_get):
        transaction = {"amount": 100, "currency": "RUB"}
        result = convert_currency(transaction)
        self.assertEqual(result, 100.0)


if __name__ == "__main__":
    unittest.main()
