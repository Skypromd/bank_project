from src.masks import get_mask_card_number  # Один импорт
from src.masks import get_mask_account  # Другой импорт
from datetime import datetime  # Третий


def mask_account_card(input_string: str) -> str:
    """
    Маскирует номер карты или счета в зависимости от типа.

    :param input_string: Строка, содержащая тип и номер карты или счета.
    :return: Замаскированный номер в формате "Тип 7000 79** **** 6361" или "Тип **4305".
    """
    parts = input_string.split()
    card_type = " ".join(parts[:-1])  # Все кроме последнего элемента
    number = parts[-1]  # Последний элемент — номер карты/счета

    if len(number) == 16:  # Предполагаем, что это номер карты
        masked_number = get_mask_card_number(int(number))
    elif len(number) >= 4:  # Предполагаем, что это номер счета
        masked_number = get_mask_account(int(number))
    else:
        raise ValueError("Неверный формат номера.")

    return f"{card_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует строку даты в формате "2024-03-11T02:26:18.671407"
    в формат "ДД.ММ.ГГГГ".

    :param date_string: Дата в строковом формате.
    :return: Дата в формате "ДД.ММ.ГГГГ".
    """
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")
