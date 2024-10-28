import json
import os


def read_json_file(file_path: str) -> list:
    """
    Читает JSON-файл и возвращает список словарей с данными о транзакциях.

    :param file_path: Путь к JSON-файлу.
    :return: Список словарей или пустой список, если файл пустой или не найден.
    """
    if not os.path.isfile(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
        except json.JSONDecodeError:
            return []
