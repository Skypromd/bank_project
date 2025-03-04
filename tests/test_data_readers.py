"""Тесты для модуля data_readers с использованием unittest."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch

import pandas as pd

from src.data_readers import read_csv_transactions, read_excel_transactions

print("Imported src.data_readers:", read_csv_transactions.__module__)


class TestDataReaders(unittest.TestCase):

    def test_read_csv_transactions_success(self):
        """Тест успешного чтения CSV-файла."""
        sample_data = [
            {"Date": "2023-01-01", "Amount": 100.0, "Description": "Salary"},
            {"Date": "2023-01-02", "Amount": -50.0, "Description": "Expense"},
        ]
        sample_df = pd.DataFrame(sample_data)

        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.return_value = sample_df
            print("Calling read_csv_transactions from:", read_csv_transactions.__module__)
            result = read_csv_transactions("data/transactions.csv")
            self.assertEqual(result, sample_data)
            mock_read_csv.assert_called_once_with("data/transactions.csv")

    def test_read_csv_transactions_file_not_found(self):
        """Тест обработки ошибки отсутствия CSV-файла."""
        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.side_effect = FileNotFoundError
            with self.assertRaises(ValueError) as cm:
                read_csv_transactions("data/transactions.csv")
            self.assertEqual(str(cm.exception), "Файл data/transactions.csv не найден")

    def test_read_csv_transactions_empty_file(self):
        """Тест обработки пустого CSV-файла."""
        with patch("pandas.read_csv") as mock_read_csv:
            mock_read_csv.side_effect = pd.errors.EmptyDataError
            result = read_csv_transactions("data/transactions.csv")
            self.assertEqual(result, [])

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
            self.assertEqual(result, sample_data)
            mock_read_excel.assert_called_once_with("data/transactions_excel.xlsx")

    def test_read_excel_transactions_file_not_found(self):
        """Тест обработки ошибки отсутствия Excel-файла."""
        with patch("pandas.read_excel") as mock_read_excel:
            mock_read_excel.side_effect = FileNotFoundError
            with self.assertRaises(ValueError) as cm:
                read_excel_transactions("data/transactions_excel.xlsx")
            self.assertEqual(str(cm.exception), "Файл data/transactions_excel.xlsx не найден")

    def test_read_excel_transactions_empty_file(self):
        """Тест обработки пустого Excel-файла."""
        with patch("pandas.read_excel") as mock_read_excel:
            mock_read_excel.side_effect = pd.errors.EmptyDataError
            result = read_excel_transactions("data/transactions_excel.xlsx")
            self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
