import unittest
import json
import os
from typing import cast, TextIO


def safe_json_dump(data, file: TextIO):
    """Обертка для json.dump с правильными типами."""
    json.dump(data, cast(TextIO, file), ensure_ascii=False, indent=4)


def load_json_file(file_path: str) -> list:
    """Загружает данные из JSON файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

