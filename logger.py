import logging
import os

# Создание папки для логов, если она не существует
os.makedirs("logs", exist_ok=True)

# Настройка логирования для модуля utils
utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)

utils_handler = logging.FileHandler("logs/utils.log")
utils_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
utils_handler.setFormatter(utils_formatter)

utils_logger.addHandler(utils_handler)

# Настройка логирования для модуля masks
masks_logger = logging.getLogger("masks")
masks_logger.setLevel(logging.DEBUG)

masks_handler = logging.FileHandler("logs/masks.log")
masks_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
masks_handler.setFormatter(masks_formatter)

masks_logger.addHandler(masks_handler)
