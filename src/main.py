# src/main.py (финальная версия)
from typing import List, Dict, Optional
from src.processing import (
    search_transactions_by_description,
    filter_by_state,
    sort_by_date,
)
from src.data_readers import read_csv_transactions, read_excel_transactions
from src.file_utils import load_json_file
from src.generators import filter_by_currency
from src.widget import get_date, mask_account_card


def main(transactions_input: Optional[List[Dict]] = None):
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакций из XLSX-файла")

    choice = input("Пользователь: ").strip()
    if transactions_input is not None:
        transactions = transactions_input
    elif choice == "1":
        try:
            transactions = load_json_file("data/transactions.json")
            print("Для обработки выбран JSON-файл.")
        except FileNotFoundError:
            print("Файл не найден. Пожалуйста, проверьте путь к файлу.")
            return
    elif choice == "2":
        transactions = read_csv_transactions("data/transactions.csv")
        print("Для обработки выбран CSV-файл.")
    elif choice == "3":
        transactions = read_excel_transactions("data/transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл.")
    else:
        print("Неверный выбор. Завершение программы.")
        return

    while True:
        status = (
            input("Введите статус для фильтрации (EXECUTED, CANCELED, PENDING): ")
            .strip()
            .upper()
        )
        if status in ["EXECUTED", "CANCELED", "PENDING"]:
            transactions = filter_by_state(transactions, status)
            print(f'Операции отфильтрованы по статусу "{status}"')
            break
        print(f'Статус операции "{status}" недоступен')

    sort_choice = input("Отсортировать операции по дате? Да/Нет: ").strip().lower()
    if sort_choice == "да":
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        reverse = order == "по убыванию"
        transactions = sort_by_date(transactions, reverse)

    rub_choice = input("Выводить только рублёвые транзакции? Да/Нет: ").strip().lower()
    if rub_choice == "да":
        transactions = list(filter_by_currency(transactions, "RUB"))

    search_choice = input("Отфильтровать по слову в описании? Да/Нет: ").strip().lower()
    if search_choice == "да":
        search_str = input("Введите строку для поиска: ").strip()
        transactions = search_transactions_by_description(transactions, search_str)

    print("Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(transactions)}")
        for t in transactions:
            date = get_date(t.get("date", "N/A"))
            amount = (
                t.get("operationAmount", {}).get("amount", "N/A")
                if "operationAmount" in t
                else t.get("amount", "N/A")
            )
            currency = (
                t.get("operationAmount", {}).get("currency", {}).get("code", "N/A")
                if "operationAmount" in t
                else t.get("currency", {}).get("code", "N/A")
            )
            from_acc = mask_account_card(t.get("from", "N/A"))
            to_acc = mask_account_card(t.get("to", "N/A"))
            print(f"{date} {t.get('description', 'N/A')}")
            print(f"{from_acc} -> {to_acc}")
            print(f"Сумма: {amount} {currency}")
            print()


if __name__ == "__main__":
    main()
