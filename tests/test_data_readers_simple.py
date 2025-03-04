import unittest

from src.data_readers import read_csv_transactions, read_excel_transactions

print("Imported src.data_readers:", read_csv_transactions.__module__)


class TestDataReadersSimple(unittest.TestCase):
    def test_import_and_call(self):
        """Простой тест для проверки импорта и вызова."""
        try:
            read_csv_transactions("nonexistent.csv")
        except ValueError:
            pass
        try:
            read_excel_transactions("nonexistent.xlsx")
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
