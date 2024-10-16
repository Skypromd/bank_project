from datetime import datetime


def mask_account_card(card_number: str) -> str:
    """Маскирует номер карты или счета.

    Args:
        card_number (str): Номер карты или счета.

    Returns:
        str: Маскированный номер карты или счета.

    Raises:
        ValueError: Если формат номера неверный.
    """
    # Извлекаем только цифры из строки
    digits = ''.join(filter(str.isdigit, card_number))

    # Проверяем длину номера карты
    if len(digits) == 16:
        # Форматирование номера карты
        masked = f"{digits[:6]} {digits[6:8]}** **** {digits[-4:]}"
        return f"{card_number.split()[0]} {masked}"

    # Проверка для номеров счетов (должно быть больше 4 цифр)
    if len(digits) > 4:
        # Форматирование номера счета, оставляя только последние 4 цифры
        return f"{card_number.split()[0]} **{digits[-4:]}"

    raise ValueError("Неверный формат номера карты или счета.")


def get_date(date_string: str) -> str:
    """Преобразует строку даты в формат 'DD.MM.YYYY'.

    Args:
        date_string (str): Дата в формате ISO.

    Returns:
        str: Дата в формате 'DD.MM.YYYY'.

    Raises:
        ValueError: Если формат даты неверный.
    """
    try:
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Неверный формат даты.")