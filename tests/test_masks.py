from src.masks import get_mask_account, get_mask_card_number


class TestMasks:
    def test_get_mask_card_number_success(self):
        """Тест успешной маскировки номера карты."""
        assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

    def test_get_mask_card_number_invalid_length(self):
        """Тест обработки номера карты неправильной длины."""
        assert get_mask_card_number("123") == "Неверный формат номера карты"

    def test_get_mask_card_number_invalid_digits(self):
        """Тест обработки номера карты с некорректными символами."""
        assert (
            get_mask_card_number("1234abcd90123456") == "Неверный формат номера карты"
        )

    def test_get_mask_account_success(self):
        """Тест успешной маскировки номера счёта."""
        assert get_mask_account("12345678901234567890") == "**7890"

    def test_get_mask_account_invalid_length(self):
        """Тест обработки номера счёта неправильной длины."""
        assert get_mask_account("123") == "Неверный формат номера счёта"
