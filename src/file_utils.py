import json
import logging
import os
from typing import TextIO

# Настройка логирования
os.makedirs("logs", exist_ok=True)

# Создание логгера для модуля utils
utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)  # Уровень логирования не меньше DEBUG

# Настройка обработчика для записи логов в файл
file_handler = logging.FileHandler('logs/utils.log', mode='w')  # Перезапись при каждом запуске
file_handler.setLevel(logging.DEBUG)

# Форматирование логов
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Добавление обработчика к логгеру
utils_logger.addHandler(file_handler)

def safe_json_dump(data, file: TextIO):
    """Обертка для json.dump с правильными типами."""
    try:
        json.dump(data, file, ensure_ascii=False, indent=4)
        utils_logger.info("Данные успешно сохранены в файл.")
    except Exception as e:
        utils_logger.error("Ошибка при сохранении данных в файл: %s", e)

def load_json_file(file_path: str) -> list:
    """Загружает данные из JSON файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            utils_logger.info("Данные успешно загружены из файла: %s", file_path)
            return data
    except FileNotFoundError:
        utils_logger.error("Файл не найден: %s", file_path)
        return []
    except json.JSONDecodeError:
        utils_logger.error("Ошибка декодирования JSON в файле: %s", file_path)
        return []
    except Exception as e:
        utils_logger.error("Ошибка при загрузке данных из файла: %s", e)
        return []