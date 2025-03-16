# src/main.py
import json
from typing import Any, Dict, List, Optional

from src.processing import filter_by_currency, filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card


def load_json_file(file_path: str = "data/transactions.json") -> List[Dict[str, Any]]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Файл не найден. Пожалуйста, проверьте путь к файлу.")
        return []
    except json.JSONDecodeError:
        print("Ошибка при чтении JSON. Проверьте формат файла.")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


def read_csv_transactions(
    file_path: str = "data/transactions.csv",
) -> List[Dict[str, Any]]:
    # Заглушка для чтения CSV
    return []


def read_excel_transactions(
    file_path: str = "data/transactions.xlsx",
) -> List[Dict[str, Any]]:
    # Заглушка для чтения Excel
    return []


def main(transactions: Optional[List[Dict[str, Any]]] = None) -> None:
    if transactions is None:
        print("Выберите источник данных:")
        print("1. JSON файл")
        print("2. CSV файл")
        print("3. Excel файл")
        choice = input("Введите номер (1-3): ").strip()

        if choice == "1":
            transactions = load_json_file()
        elif choice == "2":
            transactions = read_csv_transactions()
        elif choice == "3":
            transactions = read_excel_transactions()
        else:
            print("Неверный выбор. Завершение программы.")
            return

    # Если transactions пустой, продолжаем выполнение для проверки статуса
    status = (
        input("Введите статус для фильтрации (EXECUTED, CANCELED, PENDING): ")
        .strip()
        .upper()
    )
    if status not in ["EXECUTED", "CANCELED", "PENDING"]:
        print(f'Статус операции "{status}" недоступен')
        return

    sort_choice = input("Сортировать по дате? Да/Нет: ").strip().lower()
    sort_order = None
    if sort_choice == "да":
        sort_order = (
            input("Выберите порядок сортировки (по возрастанию/по убыванию): ")
            .strip()
            .lower()
        )

    rub_choice = input("Отфильтровать по валюте RUB? Да/Нет: ").strip().lower()
    search_choice = input("Отфильтровать по слову в описании? Да/Нет: ").strip().lower()
    search_term = None
    if search_choice == "да":
        search_term = input("Введите слово для поиска в описании: ").strip()

    # Фильтрация транзакций
    filtered_transactions = list(filter_by_state(transactions, status))

    if rub_choice == "да":
        filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))

    if search_term:
        filtered_transactions = [
            t
            for t in filtered_transactions
            if search_term.lower() in t.get("description", "").lower()
        ]

    if sort_choice == "да" and sort_order:
        reverse = sort_order == "по убыванию"
        filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse)

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")

    # Вывод деталей транзакций
    for transaction in filtered_transactions:
        date = get_date(transaction.get("date", ""))
        description = transaction.get("description", "N/A")
        amount = (
            transaction.get("operationAmount", {}).get("amount", "N/A")
            if "operationAmount" in transaction
            else transaction.get("amount", "N/A")
        )
        currency = (
            transaction.get("operationAmount", {})
            .get("currency", {})
            .get("code", "N/A")
            if "operationAmount" in transaction
            else transaction.get("currency", "N/A")
        )
        from_acc = mask_account_card(transaction.get("from", ""))
        to_acc = mask_account_card(transaction.get("to", ""))

        print(f"{date} {description}")
        print(f"{from_acc} -> {to_acc}")
        print(f"Сумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
