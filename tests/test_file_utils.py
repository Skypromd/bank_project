import json
import logging
import os
import unittest
from unittest.mock import patch

from src.file_utils import load_json_file, safe_json_dump

# Настройка логирования для тестов (в память, а не в файл)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()
logger.handlers = []  # Очистка обработчиков
memory_handler = logging.StreamHandler()
memory_handler.setLevel(logging.DEBUG)
memory_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(memory_handler)


class TestUtils(unittest.TestCase):

    def setUp(self):
        """Создание тестовых данных перед каждым тестом."""
        self.valid_data = [{"id": 1, "amount": 100.0}, {"id": 2, "amount": 200.0}]
        self.test_file = (
            "/home/mdgagauz/PycharmProjects/bank_project/logs/test_data.json"
        )
        self.empty_file = "/home/mdgagauz/PycharmProjects/bank_project/logs/empty.json"
        self.invalid_file = (
            "/home/mdgagauz/PycharmProjects/bank_project/logs/invalid.json"
        )

        # Создание тестового файла с данными
        with open(self.test_file, "w", encoding="utf-8") as f:
            safe_json_dump(self.valid_data, f)

        # Создание пустого файла
        with open(self.empty_file, "w", encoding="utf-8") as f:
            f.write("")

        # Создание файла с некорректным JSON
        with open(self.invalid_file, "w", encoding="utf-8") as f:
            f.write("invalid json")

        logger.info("Начало тестов.")

    def tearDown(self):
        """Удаление тестовых данных после каждого теста."""
        for file in [self.test_file, self.empty_file, self.invalid_file]:
            try:
                os.remove(file)
                logger.info("Удален файл: %s", file)
            except FileNotFoundError:
                logger.warning("Файл не найден для удаления: %s", file)

    def test_safe_json_dump_success(self):
        """Тест успешного сохранения JSON."""
        with open(self.test_file, "w", encoding="utf-8") as f:
            safe_json_dump(self.valid_data, f)
        with open(self.test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, self.valid_data)

    def test_safe_json_dump_error(self):
        """Тест ошибки при сохранении JSON."""
        with patch("json.dump", side_effect=Exception("Test error")):
            with open(self.test_file, "w", encoding="utf-8") as f:
                safe_json_dump(self.valid_data, f)
            # Проверяем, что файл остался пустым
            with open(self.test_file, "r", encoding="utf-8") as f:
                self.assertEqual(f.read(), "")

    def test_load_json_file_success(self):
        """Тест чтения корректного JSON файла."""
        result = load_json_file(self.test_file)
        self.assertIsInstance(result, list)
        self.assertEqual(result, self.valid_data)

    def test_empty_file(self):
        """Тест чтения пустого JSON файла."""
        result = load_json_file(self.empty_file)
        self.assertEqual(result, [])

    def test_non_existent_file(self):
        """Тест чтения несуществующего файла."""
        result = load_json_file(
            "/home/mdgagauz/PycharmProjects/bank_project/logs/non_existent.json"
        )
        self.assertEqual(result, [])

    def test_invalid_json(self):
        """Тест чтения файла с некорректным JSON."""
        result = load_json_file(self.invalid_file)
        self.assertEqual(result, [])

    def test_load_json_file_general_exception(self):
        """Тест общего исключения при загрузке JSON."""
        with patch("builtins.open", side_effect=Exception("General error")):
            result = load_json_file(self.test_file)
            self.assertEqual(result, [])

    def test_logging(self):
        """Тестирование логирования."""
        with self.assertLogs("root", level="INFO") as cm:
            load_json_file(self.test_file)
            self.assertIn("Данные успешно загружены из файла", cm.output[0])
        with self.assertLogs("root", level="ERROR") as cm:
            load_json_file("/nonexistent.json")
            self.assertIn("Файл не найден", cm.output[0])


if __name__ == "__main__":
    logger.info("Запуск программы.")
    unittest.main(verbosity=2)
