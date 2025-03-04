# src/file_handlers.py
from typing import Dict, List

import pandas as pd


def read_csv(file_path: str) -> List[Dict]:
    """
    Считывает данные из CSV-файла.
    """
    df = pd.read_csv(file_path)
    return df.to_dict("records")


def read_excel(file_path: str) -> List[Dict]:
    """
    Считывает данные из Excel-файла.
    """
    df = pd.read_excel(file_path)
    return df.to_dict("records")
