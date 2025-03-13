# tests/test_data_readers.py
import pandas as pd
from unittest.mock import patch
import pytest
from src.data_readers import read_csv_transactions, read_excel_transactions

class TestDataReaders:
    def test_read_csv_transactions_empty_file(self):
        """Тест обработки пустого CSV-файла."""
        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.side_effect = pd.errors.EmptyDataError
            result = read_csv_transactions("data/transactions.csv")
            assert result == []

    def test_read_csv_transactions_file_not_found(self):
        """Тест обработки ошибки отсутствия CSV-файла."""
        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.side_effect = FileNotFoundError
            with pytest.raises(ValueError) as cm:
                read_csv_transactions("data/transactions.csv")
            assert str(cm.value) == "Файл data/transactions.csv не найден"

    def test_read_csv_transactions_success(self):
        """Тест успешного чтения CSV-файла."""
        sample_data = [
            {"Date": "2023-01-01", "Amount": 100.0, "Description": "Salary"},
            {"Date": "2023-01-02", "Amount": -50.0, "Description": "Expense"},
        ]
        sample_df = pd.DataFrame(sample_data)

        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.return_value = sample_df
            result = read_csv_transactions("data/transactions.csv")
            assert result == sample_data
            mock_read_csv.assert_called_once_with("data/transactions.csv", delimiter=';')

    def test_read_excel_transactions_empty_file(self):
        """Тест обработки пустого Excel-файла."""
        with patch("pandas.read_excel") as mock_read_excel:
            mock_read_excel.side_effect = pd.errors.EmptyDataError
            result = read_excel_transactions("data/transactions_excel.xlsx")
            assert result == []

    def test_read_excel_transactions_file_not_found(self):
        """Тест обработки ошибки отсутствия Excel-файла."""
        with patch("pandas.read_excel") as mock_read_excel:
            mock_read_excel.side_effect = FileNotFoundError
            with pytest.raises(ValueError) as cm:
                read_excel_transactions("data/transactions_excel.xlsx")
            assert str(cm.value) == "Файл data/transactions_excel.xlsx не найден"

    def test_read_excel_transactions_success(self):
        """Тест успешного чтения Excel-файла."""
        sample_data = [
            {"Date": "2023-01-01", "Amount": 100.0, "Description": "Salary"},
            {"Date": "2023-01-02", "Amount": -50.0, "Description": "Expense"},
        ]
        sample_df = pd.DataFrame(sample_data)

        with patch("pandas.read_excel") as mock_read_excel:
            mock_read_excel.return_value = sample_df
            result = read_excel_transactions("data/transactions_excel.xlsx")
            assert result == sample_data
            mock_read_excel.assert_called_once_with("data/transactions_excel.xlsx")
