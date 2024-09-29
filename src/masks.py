def get_mask_card_number(card_number: int) -> str:
    """
    def get_mask_card_number(card_number):- Это объявление функции с названием `get_mask_card_number`,
    которая принимает один аргумент `card_number` - номер банковской карты.

    Маскирует номер банковской карты, оставляя видимыми первые 6 и последние 4 цифры.

    :param card_number: Номер карты в виде целого числа.
    :return: Замаскированный номер карты в формате XXXX XX** **** XXXX.
    """
    # Преобразуем номер карты в строку
    card_number_str = str(card_number)

    # Проверка длины номера карты
    if len(card_number_str) != 16 or not card_number_str.isdigit():
        raise ValueError("Номер карты должен содержать 16 цифр.")

    # Форматирование замаскированного номера карты
    masked_number = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"
    return masked_number


def get_mask_account(account_number: int) -> str:
    """
    Маскирует номер банковского счета, оставляя видимыми последние 4 цифры.

    :param account_number: Номер счета в виде целого числа.
    :return: Замаскированный номер счета в формате **XXXX.
    """
    # Преобразуем номер счета в строку
    account_number_str = str(account_number)

    # Проверка длины номера счета
    if len(account_number_str) < 4 or not account_number_str.isdigit():
        raise ValueError("Номер счета должен содержать хотя бы 4 цифры.")

    # Форматирование замаскированного номера счета
    masked_account = f"**{account_number_str[-4:]}"
    return masked_account
