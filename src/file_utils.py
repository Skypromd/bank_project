import unittest
import json
import os
from typing import cast, TextIO

def safe_json_dump(data, file: TextIO):
    """Обертка для json.dump с правильными типами."""
    json.dump(data, cast(TextIO, file), ensure_ascii=False, indent=4)

def load_json_file(file_path: str) -> list:
    """Загружает данные из JSON файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

class TestUtils(unittest.TestCase):

    def setUp(self):
        """Создание тестовых данных перед каждым тестом."""
        self.valid_data = [{"id": 1, "amount": 100.0}, {"id": 2, "amount": 200.0}]
        os.makedirs("data", exist_ok=True)  # Создание директории, если она не существует

        with open("data/operations.json", "w", encoding="utf-8") as f:
            safe_json_dump(self.valid_data, f)

        # Создание пустого файла
        with open("data/empty.json", "w") as f:
            f.write("")

    def tearDown(self):
        """Удаление тестовых данных после каждого теста."""
        for filename in ["operations.json", "empty.json", "invalid.json"]:
            try:
                os.remove(f"data/{filename}")
            except FileNotFoundError:
                continue

    def test_load_json_file(self):
        """Тест чтения корректного JSON файла."""
        result = load_json_file("data/operations.json")
        self.assertIsInstance(result, list)
        self.assertEqual(result, self.valid_data)

    def test_empty_file(self):
        """Тест чтения пустого JSON файла."""
        result = load_json_file("data/empty.json")
        self.assertEqual(result, [])

    def test_non_existent_file(self):
        """Тест чтения несуществующего файла."""
        result = load_json_file("data/non_existent.json")
        self.assertEqual(result, [])

    def test_invalid_json(self):
        """Тест чтения файла с некорректным JSON."""
        with open("data/invalid.json", "w", encoding="utf-8") as f:
            f.write("invalid json")

        result = load_json_file("data/invalid.json")
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
