import unittest
from unittest.mock import patch

import pandas as pd

from src.file_handlers import read_csv, read_excel


class TestFileHandlers(unittest.TestCase):

    @patch("pandas.read_csv")
    def test_read_csv(self, mock_read_csv):
        """Тест чтения финансовых операций из CSV-файла."""
        # Настраиваем мок для pd.read_csv
        mock_df = pd.DataFrame({"id": [1], "date": ["2023-01-01"], "amount": [100.50], "currency": ["USD"]})
        mock_read_csv.return_value = mock_df
        expected = [{"id": 1, "date": "2023-01-01", "amount": 100.50, "currency": "USD"}]
        result = read_csv("dummy_path.csv")
        self.assertEqual(result, expected, "Ошибка: CSV не прочитан корректно как список словарей")

    @patch("pandas.read_excel")
    def test_read_excel(self, mock_read_excel):
        """Тест чтения финансовых операций из Excel-файла."""
        # Настраиваем мок для pd.read_excel
        mock_df = pd.DataFrame({"id": [2], "date": ["2023-01-02"], "amount": [200.75], "currency": ["EUR"]})
        mock_read_excel.return_value = mock_df
        expected = [{"id": 2, "date": "2023-01-02", "amount": 200.75, "currency": "EUR"}]
        result = read_excel("dummy_path.xlsx")
        self.assertEqual(result, expected, "Ошибка: Excel не прочитан корректно как список словарей")


if __name__ == "__main__":
    unittest.main(verbosity=2)
