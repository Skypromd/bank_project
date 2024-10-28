import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_currency(transaction: dict) -> float:
    """
    Конвертирует сумму транзакции из USD или EUR в рубли.

    :param transaction: Словарь с данными о транзакции.
    :return: Сумма в рублях (float).
    """
    amount = transaction.get("amount")
    currency = transaction.get("currency")

    if amount is None:
        raise ValueError("Сумма транзакции отсутствует.")

    if currency == "RUB":
        return float(amount)

    if currency in ["USD", "EUR"]:
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API_KEY не найдена в переменных окружения.")

        response = requests.get(API_URL, params={
            "from": currency,
            "to": "RUB",
            "amount": amount
        }, headers={"apikey": api_key})

        if response.status_code != 200:
            raise Exception(f"Ошибка API: {response.status_code} - {response.text}")

        return response.json().get("result", 0.0)

    raise ValueError("Недопустимая валюта.")