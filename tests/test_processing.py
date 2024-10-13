# tests/test_processing.py
from typing import Dict, List, Union

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def transactions() -> List[Dict[str, Union[str, int]]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-02"},
        {"id": 3, "state": "EXECUTED", "date": "2023-02-01"},
    ]


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "EXECUTED",
            [
                {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
                {"id": 3, "state": "EXECUTED", "date": "2023-02-01"},
            ],
        ),
        ("CANCELED", [{"id": 2, "state": "CANCELED", "date": "2023-01-02"}]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(
    transactions: List[Dict[str, Union[str, int]]], state: str, expected: List[Dict[str, Union[str, int]]]
) -> None:
    result = filter_by_state(transactions, state)
    assert result == expected


def test_sort_by_date(transactions: List[Dict[str, Union[str, int]]]) -> None:
    sorted_result = sort_by_date(transactions)
    assert sorted_result[0]["date"] == "2023-02-01"  # Проверка на сортировку
