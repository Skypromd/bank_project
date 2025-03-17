# tests/test_main.py
import io
from unittest.mock import patch

import src.main


class TestMain:
    def test_main_invalid_choice(self):
        with patch("builtins.input", return_value="4"):
            with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                src.main.main()
                assert "Неверный выбор. Завершение программы." in mock_stdout.getvalue()

    def test_main_json_file_not_found(self):
        with patch(
            "builtins.input", side_effect=["1", "EXECUTED", "нет", "нет", "нет"]
        ):
            with patch("src.main.load_json_file", return_value=[]):
                with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                    src.main.main()
                    output = mock_stdout.getvalue()
                    assert (
                        "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
                        in output
                    )

    def test_main_invalid_status_empty_list(self):
        transactions = []
        with patch(
            "builtins.input",
            side_effect=["1", "INVALID", "EXECUTED", "нет", "нет", "нет"],
        ):
            with patch("src.main.load_json_file", return_value=transactions):
                with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                    src.main.main()
                    assert (
                        'Статус операции "INVALID" недоступен' in mock_stdout.getvalue()
                    )

    def test_main_with_input_data(self):
        transactions = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Тест",
                "state": "EXECUTED",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch("builtins.input", side_effect=["EXECUTED", "нет", "нет", "нет"]):
            with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                src.main.main(transactions)
                assert (
                    "Всего банковских операций в выборке: 1" in mock_stdout.getvalue()
                )

    def test_main_with_sorting(self):
        transactions = [
            {
                "date": "2023-01-02T00:00:00",
                "description": "Тест2",
                "state": "EXECUTED",
                "operationAmount": {"amount": "200", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            },
            {
                "date": "2023-01-01T00:00:00",
                "description": "Тест1",
                "state": "EXECUTED",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            },
        ]
        with patch(
            "builtins.input",
            side_effect=["EXECUTED", "да", "по возрастанию", "нет", "нет"],
        ):
            with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                src.main.main(transactions)
                output = mock_stdout.getvalue()
                assert "2023-01-01 Тест1" in output
                assert "2023-01-02 Тест2" in output

    def test_main_with_direct_amount(self):
        transactions = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Тест",
                "state": "EXECUTED",
                "amount": "100",
                "currency": "RUB",
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch("builtins.input", side_effect=["EXECUTED", "нет", "нет", "нет"]):
            with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                src.main.main(transactions)
                assert "Сумма: 100 RUB" in mock_stdout.getvalue()

    def test_main_with_direct_currency(self):
        transactions = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Тест",
                "state": "EXECUTED",
                "amount": "100",
                "currency": "RUB",
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch("builtins.input", side_effect=["EXECUTED", "нет", "нет", "нет"]):
            with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                src.main.main(transactions)
                assert "Сумма: 100 RUB" in mock_stdout.getvalue()

    def test_main_with_empty_fields(self):
        transactions = [
            {
                "date": "",
                "description": "",
                "state": "EXECUTED",
                "operationAmount": {},
                "from": "",
                "to": "",
            }
        ]
        with patch("builtins.input", side_effect=["EXECUTED", "нет", "нет", "нет"]):
            with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                src.main.main(transactions)
                assert "N/A N/A" in mock_stdout.getvalue()
                assert (
                    "Неверный формат номера карты -> Неверный формат номера карты"
                    in mock_stdout.getvalue()
                )
                assert "Сумма: N/A N/A" in mock_stdout.getvalue()

    def test_main_with_max_description(self):
        transactions = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Тест " * 100,
                "state": "EXECUTED",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch("builtins.input", side_effect=["EXECUTED", "нет", "нет", "нет"]):
            with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                src.main.main(transactions)
                assert "Тест " * 100 in mock_stdout.getvalue()

    def test_main_json_executed_rub_search(self):
        transactions = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Перевод",
                "state": "EXECUTED",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            },
            {
                "date": "2023-01-02T00:00:00",
                "description": "Пополнение",
                "state": "EXECUTED",
                "operationAmount": {"amount": "200", "currency": {"code": "USD"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            },
        ]
        with patch(
            "builtins.input",
            side_effect=["1", "EXECUTED", "нет", "да", "да", "Перевод", "нет"],
        ):
            with patch("src.main.load_json_file", return_value=transactions):
                with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                    src.main.main()
                    assert (
                        "Всего банковских операций в выборке: 1"
                        in mock_stdout.getvalue()
                    )
                    assert "Перевод" in mock_stdout.getvalue()
                    assert "Сумма: 100 RUB" in mock_stdout.getvalue()

    def test_main_csv_canceled_no_sort(self):
        transactions = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Перевод",
                "state": "CANCELED",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            },
            {
                "date": "2023-01-02T00:00:00",
                "description": "Пополнение",
                "state": "EXECUTED",
                "operationAmount": {"amount": "200", "currency": {"code": "USD"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            },
        ]
        with patch(
            "builtins.input", side_effect=["2", "CANCELED", "нет", "нет", "нет"]
        ):
            with patch("src.main.read_csv_transactions", return_value=transactions):
                with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                    src.main.main()
                    assert (
                        "Всего банковских операций в выборке: 1"
                        in mock_stdout.getvalue()
                    )
                    assert "Перевод" in mock_stdout.getvalue()

    def test_main_excel_pending_sort_desc_rub(self):
        transactions = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Перевод",
                "state": "PENDING",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            },
            {
                "date": "2023-01-02T00:00:00",
                "description": "Пополнение",
                "state": "PENDING",
                "operationAmount": {"amount": "200", "currency": {"code": "USD"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            },
        ]
        with patch(
            "builtins.input",
            side_effect=["3", "PENDING", "да", "по убыванию", "да", "нет", "нет"],
        ):
            with patch("src.main.read_excel_transactions", return_value=transactions):
                with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                    src.main.main()
                    assert (
                        "Всего банковских операций в выборке: 1"
                        in mock_stdout.getvalue()
                    )
                    assert "2023-01-01 Перевод" in mock_stdout.getvalue()
                    assert "Сумма: 100 RUB" in mock_stdout.getvalue()

    def test_main_empty_filtered_list_rub(self):
        transactions = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Перевод",
                "state": "EXECUTED",
                "operationAmount": {"amount": "100", "currency": {"code": "USD"}},
                "from": "Счет 1234",
                "to": "Счет 5678",
            }
        ]
        with patch(
            "builtins.input",
            side_effect=["1", "EXECUTED", "нет", "да", "нет", "нет", "нет"],
        ):
            with patch("src.main.load_json_file", return_value=transactions):
                with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                    src.main.main()
                    assert (
                        "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
                        in mock_stdout.getvalue()
                    )

    def test_main_empty_input(self):
        """Тест обработки пустого ввода."""
        with patch(
            "builtins.input",
            side_effect=["", "1", "EXECUTED", "нет", "нет", "нет", "нет"],
        ):
            with patch("src.main.load_json_file", return_value=[]):
                with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                    src.main.main()
                    assert (
                        "Неверный выбор. Завершение программы."
                        in mock_stdout.getvalue()
                    )

    def test_main_all_inputs(self):
        """Тест обработки всех возможных ответов."""
        transactions = [
            {
                "date": "2023-01-01T00:00:00",
                "description": "Тест",
                "state": "EXECUTED",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
                "from": "Счет 1234567890123456",
                "to": "Счет 5678",
            }
        ]
        with patch(
            "builtins.input",
            side_effect=["1", "EXECUTED", "да", "по убыванию", "да", "тест", "нет"],
        ):
            with patch("src.main.load_json_file", return_value=transactions):
                with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
                    src.main.main()
                    output = mock_stdout.getvalue()
                    assert "Всего банковских операций в выборке: 1" in output
                    assert "Счет 123456 78** **** 3456" in output  # Проверка маскировки
