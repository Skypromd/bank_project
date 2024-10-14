import unittest

from main import get_date, mask_account_card


class TestBankOperations(unittest.TestCase):
    def test_mask_account_card(self) -> None:
        # Тест для номера карты
        self.assertEqual(mask_account_card("Карта 1234567812345678"), "Карта 123456 78** **** 5678")

        # Тест для номера счета
        self.assertEqual(mask_account_card("Счет 1234567890123456"), "Счет **3456")

        # Тест для некорректного формата
        with self.assertRaises(ValueError):
            mask_account_card("Карта 12345")  # Неверный формат

    def test_get_date(self) -> None:
        # Тест корректного преобразования даты
        self.assertEqual(get_date("2024-03-11T02:26:18.671407"), "11.03.2024")

        # Тест для некорректного формата даты
        with self.assertRaises(ValueError):
            get_date("Неверная дата")  # Неверный формат даты


if __name__ == "__main__":
    unittest.main()
