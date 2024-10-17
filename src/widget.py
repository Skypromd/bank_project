from datetime import datetime  # Третий


def mask_account_card(card_number: str) -> str:
    """Маскирует номер банковской карты, оставляя видимыми первые 6 и последние 4 цифры."""
    # Убираем все нецифровые символы
    card_number_digits = "".join([char for char in card_number if char.isdigit()])

    # Проверка длины номера карты
    if len(card_number_digits) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр.")

    # Форматирование замаскированного номера карты
    masked_number = f"{card_number_digits[:6]} {card_number_digits[6:8]}** **** {card_number_digits[-4:]}"
    return masked_number


def get_date(date_string: str) -> str:
    """
    Преобразует строку даты в формате "2024-03-11T02:26:18.671407"
    в формат "ДД.ММ.ГГГГ".

    :param date_string: Дата в строковом формате.
    :return: Дата в формате "ДД.ММ.ГГГГ".
    """
    dt = datetime.fromisoformat(date_string)
    return dt.strftime("%d.%m.%Y")
