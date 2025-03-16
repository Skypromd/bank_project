# tests/test_processing.py
from src.processing import filter_by_currency, filter_by_state, sort_by_date


class TestProcessing:
    def test_filter_by_currency(self):
        transactions = [
            {"operationAmount": {"currency": {"code": "RUB"}}},
            {"operationAmount": {"currency": {"code": "USD"}}},
        ]
        result = list(filter_by_currency(transactions, "RUB"))
        assert len(result) == 1
        assert result[0]["operationAmount"]["currency"]["code"] == "RUB"

    def test_filter_by_currency_direct(self):
        transactions = [
            {"operationAmount": {"currency": "RUB"}},
            {"operationAmount": {"currency": "USD"}},
        ]
        result = list(filter_by_currency(transactions, "RUB"))
        assert len(result) == 1
        assert result[0]["operationAmount"]["currency"] == "RUB"

    def test_filter_by_state_canceled(self):
        transactions = [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T00:00:00",
                "description": "Тест1",
            },
            {
                "id": 2,
                "state": "CANCELED",
                "date": "2023-01-02T00:00:00",
                "description": "Тест2",
            },
        ]
        result = filter_by_state(transactions, "CANCELED")
        assert result == [
            {
                "id": 2,
                "state": "CANCELED",
                "date": "2023-01-02T00:00:00",
                "description": "Тест2",
            }
        ]

    def test_filter_by_state_executed(self):
        transactions = [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T00:00:00",
                "description": "Тест1",
            },
            {
                "id": 2,
                "state": "CANCELED",
                "date": "2023-01-02T00:00:00",
                "description": "Тест2",
            },
        ]
        result = filter_by_state(transactions, "EXECUTED")
        assert result == [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T00:00:00",
                "description": "Тест1",
            }
        ]

    def test_filter_by_state_unknown(self):
        transactions = [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T00:00:00",
                "description": "Тест1",
            },
            {
                "id": 2,
                "state": "CANCELED",
                "date": "2023-01-02T00:00:00",
                "description": "Тест2",
            },
        ]
        result = filter_by_state(transactions, "UNKNOWN")
        assert result == []

    def test_sort_by_date(self):
        transactions = [
            {"date": "2023-01-02T00:00:00", "description": "Тест2"},
            {"date": "2023-01-01T00:00:00", "description": "Тест1"},
        ]
        result_asc = sort_by_date(transactions, reverse=False)
        assert result_asc[0]["description"] == "Тест1"
        assert result_asc[1]["description"] == "Тест2"

        result_desc = sort_by_date(transactions, reverse=True)
        assert result_desc[0]["description"] == "Тест2"
        assert result_desc[1]["description"] == "Тест1"
