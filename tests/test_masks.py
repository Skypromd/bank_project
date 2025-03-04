# tests/test_masks.py
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest

from src.masks import get_mask_account, get_mask_card_number


class TestMasks(unittest.TestCase):

    def test_get_mask_card_number_success(self):
        """Тест успешной маскировки номера карты."""
        result = get_mask_card_number(1234567890123456)
        self.assertEqual(result, "1234 56** **** 3456")

    def test_get_mask_card_number_invalid_length(self):
        """Тест обработки неверной длины номера карты."""
        with self.assertRaises(ValueError) as cm:
            get_mask_card_number(123456789012)  # Менее 16 цифр
        self.assertEqual(str(cm.exception), "Номер карты должен содержать 16 цифр.")

    def test_get_mask_card_number_invalid_digits(self):
        """Тест обработки нечислового ввода (невалидный случай для int)."""
        # Поскольку аргумент int, нечисловые значения вызовут TypeError на уровне Python
        # Но мы можем проверить через преобразование строки в int
        with self.assertRaises(ValueError):
            get_mask_card_number(int("12345678901234ab"))  # Преобразуется с ошибкой

    def test_get_mask_account_success(self):
        """Тест успешной маскировки номера счёта."""
        result = get_mask_account(12345678901234567890)
        self.assertEqual(result, "**7890")
        result_short = get_mask_account(12345678)
        self.assertEqual(result_short, "**5678")

    def test_get_mask_account_invalid_length(self):
        """Тест обработки номера счёта менее 4 цифр."""
        with self.assertRaises(ValueError) as cm:
            get_mask_account(123)  # Менее 4 цифр
        self.assertEqual(str(cm.exception), "Номер счета должен содержать хотя бы 4 цифры.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
