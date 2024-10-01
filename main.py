from src.widget import get_date, mask_account_card

if __name__ == "__main__":
    # Примеры входных данных для проверки функции  mask_account_card
    test_cases = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]

    for case in test_cases:
        masked_result = mask_account_card(case)
        print(f"{case} -> {masked_result}")

    # Пример использования функции get_date
    print(get_date("2024-03-11T02:26:18.671407"))  # Ожидаемый вывод: 11.03.2024

# main.py

from src.processing import filter_by_state, sort_by_date


def main():
    # Пример списка операций
    transactions = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    # Фильтрация операций по значению 'EXECUTED'
    executed_transactions = filter_by_state(transactions)
    print("Фильтрованные операции (EXECUTED):")
    print(executed_transactions)

    # Сортировка операций по дате
    sorted_transactions = sort_by_date(transactions)
    print("\nСортированные операции (по убыванию даты):")
    print(sorted_transactions)


if __name__ == "__main__":
    main()
