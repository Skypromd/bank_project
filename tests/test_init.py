import unittest

import src  # Импорт пакета src


class TestInit(unittest.TestCase):

    def test_convert_currency(self):
        """Тест функции convert_currency из __init__.py."""
        result = src.convert_currency()
        self.assertIsNone(result, "convert_currency должен возвращать None")

    def test_get_conversion_rate(self):
        """Тест функции get_conversion_rate из __init__.py."""
        result = src.get_conversion_rate()
        self.assertIsNone(result, "get_conversion_rate должен возвращать None")

    def test_external_api(self):
        """Тест функции external_api из __init__.py."""
        result = src.external_api()
        self.assertIsNone(result, "external_api должен возвращать None")


if __name__ == "__main__":
    unittest.main(verbosity=2)
