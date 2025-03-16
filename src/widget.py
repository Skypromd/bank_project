# src/widget.py
from datetime import datetime


def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой в формат ГГГГ-ММ-ДД.

    :param date_str: Строка с датой в формате ISO (например, "2023-01-01T12:00:00").
    :return: Отформатированная дата или "N/A" при ошибке.
    """
    if not date_str or not isinstance(date_str, str):
        return "N/A"
    try:
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return date_obj.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return "N/A"


def mask_account_card(card_info: str) -> str:
    """
    Маскирует номер карты или счета.

    :param card_info: Строка с информацией о карте или счёте (например, "Visa 1234567890123456").
    :return: Замаскированная строка или сообщение об ошибке.
    """
    if not card_info or not isinstance(card_info, str):
        return "Неверный формат номера карты"

    parts = card_info.split()
    if len(parts) < 1:
        return "Неверный формат номера карты"

    number = parts[-1].replace(" ", "")
    if not number.isdigit():
        return "Неверный формат номера карты"

    if len(number) == 16:
        return f"{parts[0]} {number[:6]} {number[6:8]}** **** {number[-4:]}"
    elif len(number) >= 4:
        if len(number) > 4:
            visible_part = number[:4]  # Первые 4 символа видны
            masked_part = (
                "** " + number[-4:]
            )  # Маскируем всё, кроме первых 4 и последних 4 символов с пробелом
            return (
                f"{parts[0]} {visible_part}{masked_part}"
                if len(parts) > 1
                else f"{visible_part}{masked_part}"
            )
        return "Неверный формат номера карты"
    return "Неверный формат номера карты"
