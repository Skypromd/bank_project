# src/widget.py
def get_date(date_str: str) -> str:
    """Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_str: Строка с датой в формате ISO.

    Returns:
        Дата в формате ДД.ММ.ГГГГ или 'N/A' при некорректных данных.

    Raises:
        ValueError: Если формат даты некорректен.
    """
    if not date_str or not isinstance(date_str, str):
        return "N/A"
    from datetime import datetime

    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return date_obj.strftime("%d.%m.%Y")


def mask_account_card(input_string: str) -> str:
    """Маскирует номер карты или счёта.

    Args:
        input_string: Строка с номером карты или счёта (например, 'Maestro 1596837868705199').

    Returns:
        Замаскированный номер (например, 'Maestro 1596 83** **** 5199') или сообщение об ошибке.
    """
    if not isinstance(input_string, str) or not input_string.strip():
        return "Invalid input format"
    parts = input_string.split()
    if not parts:  # Проверка на пустой список
        return "Invalid input format"
    if len(parts) == 1:
        if len(parts[0]) >= 16 and parts[0][-16:].isdigit():
            name = parts[0][:-16]
            number = parts[0][-16:]
            return f"{name} {number[:4]} {number[4:6]}** **** {number[-4:]}"
        return "Invalid input format"
    number = parts[-1]
    if not number.isdigit() or len(number) < 4:
        return "Invalid input format"
    if "Счет" in input_string:
        return f"{' '.join(parts[:-1])} **{number[-4:]}"
    if len(number) >= 16:
        return f"{' '.join(parts[:-1])} {number[:4]} {number[4:6]}** **** {number[-4:]}"
    return "Invalid input format"
