# tests/test_main.py
import sys
import os
from io import StringIO
from unittest.mock import patch
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import src.main


def generate_input(choice: str, status: str, *args: str) -> list[str]:
    """Генерирует список для side_effect с заданным выбором, статусом и дополнительными значениями.

    Args:
        choice (str): Выбор источника данных (например, "1" для JSON).
        status (str): Статус для фильтрации (EXECUTED, CANCELED, PENDING).
        *args (str): Дополнительные входные данные (например, "да", "нет", поисковая строка).

    Returns:
        list[str]: Список значений для side_effect.
    """
    return [choice, status] + list(args)


class TestMain(unittest.TestCase):

    def test_main_json_executed_rub_search(self):
        """Тест обработки JSON-файла с фильтром по статусу и описанию."""
        mock_data = [
            {
                "date": "2019-12-08T12:00:00",
                "description": "Открытие вклада",
                "state": "EXECUTED",
                "operationAmount": {"amount": "40542", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            },
            {
                "date": "2019-11-12T12:00:00",
                "description": "Перевод с карты",
                "state": "EXECUTED",
                "operationAmount": {"amount": "130", "currency": {"code": "USD"}},
                "from": "MasterCard 7771",
                "to": "Visa 1293",
            },
        ]
        with patch("src.main.load_json_file", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input(
                "1", "EXECUTED", "нет", "нет", "да", "Открытие вклада"
            ),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Всего банковских операций в выборке: 1", output)
            self.assertIn("Открытие вклада", output)
            self.assertIn("40542 RUB", output)
            self.assertIn("Для обработки выбран JSON-файл.", output)

    def test_main_csv_canceled_no_sort(self):
        """Тест обработки CSV-файла без сортировки."""
        mock_data = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Пополнение",
                "state": "CANCELED",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch("src.main.read_csv_transactions", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input("2", "CANCELED", "нет", "нет", "нет"),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Всего банковских операций в выборке: 1", output)
            self.assertIn("Пополнение", output)
            self.assertIn("Для обработки выбран CSV-файл.", output)

    def test_main_excel_pending_sort_desc_rub(self):
        """Тест обработки XLSX-файла с сортировкой и фильтром по рублям."""
        mock_data = [
            {
                "date": "2023-01-02T00:00:00",
                "description": "Оплата",
                "state": "PENDING",
                "operationAmount": {"amount": "50", "currency": {"code": "EUR"}},
                "from": "Visa 1234567890123456",
                "to": "Счет 5678",
            },
            {
                "date": "2023-01-01T00:00:00",
                "description": "Перевод",
                "state": "PENDING",
                "operationAmount": {"amount": "75", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            },
        ]
        with patch("src.main.read_excel_transactions", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input(
                "3", "PENDING", "да", "по убыванию", "да", "нет"
            ),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Всего банковских операций в выборке: 1", output)
            self.assertIn("Перевод", output)
            self.assertIn("Для обработки выбран XLSX-файл.", output)

    def test_main_invalid_choice(self):
        """Тест обработки некорректного выбора."""
        with patch("builtins.input", side_effect=generate_input("4", "")), patch(
            "sys.stdout", new_callable=StringIO
        ) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Неверный выбор. Завершение программы.", output)

    def test_main_invalid_status_empty_list(self):
        """Тест обработки некорректного статуса с пустым списком."""
        mock_data = []
        with patch("src.main.load_json_file", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input("1", "INVALID", "EXECUTED", "нет", "нет", "нет"),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn('Статус операции "INVALID" недоступен', output)
            self.assertIn("Не найдено ни одной транзакции", output)

    def test_main_empty_filtered_list_rub(self):
        """Тест обработки пустого списка после фильтрации по рублям."""
        mock_data = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Тест",
                "state": "EXECUTED",
                "operationAmount": {"amount": "100", "currency": {"code": "USD"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch("src.main.load_json_file", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input("1", "EXECUTED", "нет", "да", "нет"),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Не найдено ни одной транзакции", output)

    def test_main_with_sorting(self):
        """Тест обработки с сортировкой по дате."""
        mock_data = [
            {
                "date": "2023-01-02T00:00:00",
                "description": "Оплата",
                "state": "EXECUTED",
                "operationAmount": {"amount": "50", "currency": {"code": "EUR"}},
                "from": "Visa 1234567890123456",
                "to": "Счет 5678",
            },
            {
                "date": "2023-01-01T00:00:00",
                "description": "Перевод",
                "state": "EXECUTED",
                "operationAmount": {"amount": "75", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            },
        ]
        with patch("src.main.load_json_file", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input(
                "1", "EXECUTED", "да", "по возрастанию", "нет", "нет"
            ),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Всего банковских операций в выборке: 2", output)
            self.assertIn("Перевод", output)
            self.assertIn("Оплата", output)

    def test_main_with_input_data(self):
        """Тест обработки с переданными данными (transactions_input)."""
        mock_data = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Тест",
                "state": "EXECUTED",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch(
            "builtins.input",
            side_effect=generate_input("", "EXECUTED", "нет", "нет", "нет"),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main(transactions_input=mock_data)
            output = mock_stdout.getvalue()
            self.assertIn("Всего банковских операций в выборке: 1", output)
            self.assertIn("Тест", output)

    def test_main_with_direct_amount(self):
        """Тест обработки транзакции с прямым 'amount' без 'operationAmount'."""
        mock_data = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Прямая сумма",
                "state": "EXECUTED",
                "amount": "500",
                "currency": {"code": "RUB"},
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch("src.main.load_json_file", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input("1", "EXECUTED", "нет", "нет", "нет"),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Всего банковских операций в выборке: 1", output)
            self.assertIn("Прямая сумма", output)
            self.assertIn("500 RUB", output)
            self.assertIn("Для обработки выбран JSON-файл.", output)

    def test_main_simple_output(self):
        """Тест для явного покрытия вывода суммы."""
        mock_data = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Тест вывода",
                "state": "EXECUTED",
                "operationAmount": {"amount": "200", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch("src.main.load_json_file", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input("1", "EXECUTED", "нет", "нет", "нет"),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Всего банковских операций в выборке: 1", output)
            self.assertIn("Тест вывода", output)
            self.assertIn("Сумма: 200 RUB", output)
            self.assertIn("Для обработки выбран JSON-файл.", output)

    def test_main_with_direct_currency(self):
        """Тест обработки транзакции с прямым 'currency' без 'operationAmount'."""
        mock_data = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Прямая валюта",
                "state": "EXECUTED",
                "currency": {"code": "USD"},
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch("src.main.load_json_file", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input("1", "EXECUTED", "нет", "нет", "нет"),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Всего банковских операций в выборке: 1", output)
            self.assertIn("Прямая валюта", output)
            self.assertIn("Сумма: N/A USD", output)
            self.assertIn("Для обработки выбран JSON-файл.", output)

    def test_main_with_only_amount(self):
        """Тест обработки транзакции с прямым 'amount' без 'operationAmount' и 'currency'."""
        mock_data = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Только сумма",
                "state": "EXECUTED",
                "amount": "300",
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch("src.main.load_json_file", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input("1", "EXECUTED", "нет", "нет", "нет"),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Всего банковских операций в выборке: 1", output)
            self.assertIn("Только сумма", output)
            self.assertIn("Сумма: 300 N/A", output)
            self.assertIn("Для обработки выбран JSON-файл.", output)

    def test_main_json_file_not_found(self):
        """Тест обработки случая, когда JSON-файл не найден."""
        with patch("src.main.load_json_file", side_effect=FileNotFoundError), patch(
            "builtins.input", side_effect=generate_input("1", "")
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Файл не найден. Пожалуйста, проверьте путь к файлу.", output)

    def test_main_with_empty_fields(self):
        """Тест обработки транзакции с пустыми полями."""
        mock_data = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "",
                "state": "EXECUTED",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
                "from": "",
                "to": "",
            }
        ]
        with patch("src.main.load_json_file", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input("1", "EXECUTED", "нет", "нет", "нет"),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Всего банковских операций в выборке: 1", output)
            self.assertIn("01.01.2023 ", output)
            self.assertIn("Invalid input format -> Invalid input format", output)
            self.assertIn("Сумма: 100 RUB", output)

    def test_main_with_max_description(self):
        """Тест обработки транзакции с длинным описанием."""
        long_desc = "A" * 1000  # Максимально длинное описание
        mock_data = [
            {
                "date": "2023-01-01T00:00:00",
                "description": long_desc,
                "state": "EXECUTED",
                "operationAmount": {"amount": "999999999", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch("src.main.load_json_file", return_value=mock_data), patch(
            "builtins.input",
            side_effect=generate_input("1", "EXECUTED", "нет", "нет", "нет"),
        ), patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            src.main.main()
            output = mock_stdout.getvalue()
            self.assertIn("Всего банковских операций в выборке: 1", output)
            self.assertIn(f"01.01.2023 {long_desc}", output)
            self.assertIn("Счет **1234 -> Счет **5678", output)
            self.assertIn("Сумма: 999999999 RUB", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
