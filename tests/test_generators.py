import os
import sys
import unittest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestGenerators(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            {"operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 1"},
            {"operationAmount": {"currency": {"code": "EUR"}}, "description": "Payment 2"},
            {"operationAmount": {"currency": {"code": "USD"}}, "description": "Payment 3"},
        ]

    def test_filter_by_currency(self):
        """Тест фильтрации транзакций по валюте."""
        usd_result = list(filter_by_currency(self.transactions, "USD"))
        self.assertEqual(len(usd_result), 2)
        self.assertEqual(usd_result, [self.transactions[0], self.transactions[2]])

        eur_result = list(filter_by_currency(self.transactions, "EUR"))
        self.assertEqual(len(eur_result), 1)
        self.assertEqual(eur_result, [self.transactions[1]])

        none_result = list(filter_by_currency(self.transactions, "JPY"))
        self.assertEqual(len(none_result), 0)

    def test_transaction_descriptions(self):
        """Тест генератора описаний транзакций."""
        desc_result = list(transaction_descriptions(self.transactions))
        self.assertEqual(desc_result, ["Payment 1", "Payment 2", "Payment 3"])

    def test_card_number_generator(self):
        """Тест генератора номеров карт."""
        card_numbers = list(card_number_generator(1234567890123456, 1234567890123458))
        self.assertEqual(len(card_numbers), 3)
        self.assertEqual(card_numbers, [
            "1234 5678 9012 3456",
            "1234 5678 9012 3457",
            "1234 5678 9012 3458",
        ])


if __name__ == "__main__":
    unittest.main(verbosity=2)