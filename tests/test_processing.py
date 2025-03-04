import unittest

from src.processing import filter_by_currency, filter_by_state, sort_by_date

# Тестовые данные
transactions = [
    {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "operationAmount": {"currency": {"code": "USD"}}},
    {"id": 2, "state": "CANCELED", "date": "2023-01-02", "operationAmount": {"currency": {"code": "EUR"}}},
    {"id": 3, "state": "EXECUTED", "date": "2023-02-01", "operationAmount": {"currency": {"code": "USD"}}},
]


class TestProcessing(unittest.TestCase):

    def test_filter_by_state_executed(self):
        expected = [
            {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "operationAmount": {"currency": {"code": "USD"}}},
            {"id": 3, "state": "EXECUTED", "date": "2023-02-01", "operationAmount": {"currency": {"code": "USD"}}},
        ]
        result = filter_by_state(transactions, "EXECUTED")
        self.assertEqual(result, expected)

    def test_filter_by_state_canceled(self):
        expected = [
            {"id": 2, "state": "CANCELED", "date": "2023-01-02", "operationAmount": {"currency": {"code": "EUR"}}}
        ]
        result = filter_by_state(transactions, "CANCELED")
        self.assertEqual(result, expected)

    def test_filter_by_state_unknown(self):
        expected = []
        result = filter_by_state(transactions, "UNKNOWN")
        self.assertEqual(result, expected)

    def test_sort_by_date(self):
        # По убыванию
        sorted_desc = sort_by_date(transactions, descending=True)
        self.assertEqual(sorted_desc[0]["date"], "2023-02-01")
        self.assertEqual(sorted_desc[-1]["date"], "2023-01-01")
        # По возрастанию
        sorted_asc = sort_by_date(transactions, descending=False)
        self.assertEqual(sorted_asc[0]["date"], "2023-01-01")
        self.assertEqual(sorted_asc[-1]["date"], "2023-02-01")

    def test_filter_by_currency(self):
        # USD
        usd_result = list(filter_by_currency(transactions, "USD"))
        self.assertEqual(len(usd_result), 2)
        self.assertEqual(usd_result, [transactions[0], transactions[2]])
        # EUR
        eur_result = list(filter_by_currency(transactions, "EUR"))
        self.assertEqual(len(eur_result), 1)
        self.assertEqual(eur_result, [transactions[1]])
        # JPY (несуществующая валюта)
        none_result = list(filter_by_currency(transactions, "JPY"))
        self.assertEqual(len(none_result), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
