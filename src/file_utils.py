import json
import logging

from src.config import LOGS_DIR

# Создаём директорию logs, если её нет
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Путь к лог-файлу
log_file_path = LOGS_DIR / "utils.log"

# Настройка логирования
logging.basicConfig(
    filename=log_file_path,
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def safe_json_dump(data, file):
    """Сохраняет данные в формате JSON в файл с логированием."""
    try:
        json.dump(data, file, ensure_ascii=False, indent=4)
        logging.info("Данные успешно сохранены в файл.")
    except Exception as e:
        logging.error("Ошибка при сохранении данных в файл: %s", e)


def load_json_file(file_path):
    """Загружает данные из JSON файла с логированием."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logging.info("Данные успешно загружены из файла: %s", file_path)
            return data
    except FileNotFoundError:
        logging.error("Файл не найден: %s", file_path)
        return []
    except json.JSONDecodeError:
        logging.error("Ошибка декодирования JSON в файле: %s", file_path)
        return []
    except Exception as e:
        logging.error("Ошибка при загрузке данных из файла: %s", e)
        return []
