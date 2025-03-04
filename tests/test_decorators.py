# tests/test_decorators.py
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
import unittest
from io import StringIO

from src.decorators import log

print("Imported src.decorators from:", log.__module__, "at", log.__code__.co_filename)


class TestDecorators(unittest.TestCase):

    def setUp(self):
        logging.getLogger().handlers = []
        logging.getLogger().setLevel(logging.INFO)

    def tearDown(self):
        log_file = "test_log.log"
        if os.path.exists(log_file):
            os.remove(log_file)

    def test_log_without_filename_success(self):
        """Тест успешного выполнения функции без файла логов."""
        log_buffer = StringIO()
        handler = logging.StreamHandler(log_buffer)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logging.getLogger().addHandler(handler)

        @log(filename=None)
        def sample_func(x):
            return x * 2

        result = sample_func(5)
        self.assertEqual(result, 10)
        log_output = log_buffer.getvalue()
        self.assertIn("sample_func ok", log_output)
        logging.getLogger().removeHandler(handler)
        log_buffer.close()

    def test_log_with_filename_success(self):
        """Тест успешного выполнения функции с файлом логов."""
        log_file = "test_log.log"
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logging.getLogger().addHandler(handler)

        @log(filename=log_file)
        def sample_func(x):
            return x * 2

        result = sample_func(5)
        self.assertEqual(result, 10)
        logging.getLogger().removeHandler(handler)
        handler.close()
        with open(log_file, "r") as f:
            log_output = f.read()
            self.assertIn("sample_func ok", log_output)

    def test_log_with_error(self):
        """Тест обработки исключения в декорированной функции."""
        log_buffer = StringIO()
        handler = logging.StreamHandler(log_buffer)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logging.getLogger().addHandler(handler)

        @log(filename=None)
        def error_func():
            raise ValueError("Test error")

        with self.assertRaises(ValueError):
            error_func()
        log_output = log_buffer.getvalue()
        self.assertIn("error_func error: ValueError", log_output)
        self.assertIn("Inputs: (), {}", log_output)
        logging.getLogger().removeHandler(handler)
        log_buffer.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
