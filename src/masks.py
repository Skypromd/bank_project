# src/masks.py
def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, оставляя видимыми первые 6 и последние 4 цифры.

    :param card_number: Номер карты в виде строки.
    :return: Замаскированный номер карты в формате XXXX XX** **** XXXX или сообщение об ошибке.
    """
    # Убираем пробелы и преобразуем в строку
    card_number_str = str(card_number).replace(" ", "")

    # Проверка длины и формата
    if len(card_number_str) != 16 or not card_number_str.isdigit():
        return "Неверный формат номера карты"

    # Маскировка: первые 6, затем **, последние 4
    masked = (
        f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"
    )
    return masked


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета, оставляя видимыми последние 4 цифры.

    :param account_number: Номер счета в виде строки.
    :return: Замаскированный номер счета в формате **XXXX или сообщение об ошибке.
    """
    # Убираем пробелы и преобразуем в строку
    account_number_str = str(account_number).replace(" ", "")

    # Проверка длины и формата
    if len(account_number_str) < 4 or not account_number_str.isdigit():
        return "Неверный формат номера счёта"

    # Маскировка: скрываем все, кроме последних 4 цифр
    masked = "**" + account_number_str[-4:]
    return masked
