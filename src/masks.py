import logging
import os

# Создание директории для логов, если она не существует
os.makedirs("logs", exist_ok=True)

# Настройка логгера для модуля masks
masks_logger = logging.getLogger("masks")
masks_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/masks.log", mode="w")  # перезапись при каждом запуске
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

masks_logger.addHandler(file_handler)


def get_mask_card_number(card_number: int) -> str:
    """
    Маскирует номер банковской карты, оставляя видимыми первые 6 и последние 4 цифры.
    """
    card_number_str = str(card_number)
    if len(card_number_str) != 16 or not card_number_str.isdigit():
        masks_logger.error("Некорректный номер карты: %s", card_number_str)
        raise ValueError("Номер карты должен содержать 16 цифр.")

    masked_number = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"
    masks_logger.info("Замаскированный номер карты: %s", masked_number)
    return masked_number


def get_mask_account(account_number: int) -> str:
    """
    Маскирует номер банковского счета, оставляя видимыми последние 4 цифры.
    """
    account_number_str = str(account_number)

    if len(account_number_str) < 4 or not account_number_str.isdigit():
        masks_logger.error("Некорректный номер счета: %s", account_number_str)
        raise ValueError("Номер счета должен содержать хотя бы 4 цифры.")

    masked_account = f"**{account_number_str[-4:]}"
    masks_logger.info("Замаскированный номер счета: %s", masked_account)
    return masked_account
