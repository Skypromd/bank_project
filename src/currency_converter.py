import requests
from typing import Any, Dict

def get_conversion_rate(from_currency: str, to_currency: str) -> float:
    try:
        response = requests.get(
            "https://api.apilayer.com/exchangerates_data/convert",
            params={"from": from_currency, "to": to_currency, "amount": 1},
            headers={"apikey": "your_api_key_here"}  # Замените на реальный API-ключ
        )
        response.raise_for_status()
        return response.json().get("result", 0.0)  # Изменили "info" на "result"
    except requests.RequestException:
        return 0.0

def convert_currency(transaction_data: Dict[str, Any]) -> float:
    operation_amount = transaction_data.get("operationAmount")
    if not operation_amount:
        return 0.0

    amount_str = operation_amount.get("amount")
    currency = operation_amount.get("currency", {}).get("code")
    if not amount_str or not currency:
        return 0.0

    try:
        amount = float(amount_str)
        if amount < 0:
            return 0.0
    except ValueError:
        return 0.0

    if currency == "RUB":
        return amount

    supported_currencies = ["USD", "EUR"]
    if currency in supported_currencies:
        rate = get_conversion_rate(currency, "RUB")
        if rate <= 0:
            return 0.0
        return amount * rate

    return 0.0
