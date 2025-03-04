import logging
from typing import Any, Dict

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_conversion_rate(from_currency: str, to_currency: str) -> float:
    url = "https://api.exchangerate-api.com/v4/latest/" + from_currency
    params: dict[str, str] = {"base": from_currency, "symbols": to_currency}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"API response: {data}")
        if "info" in data and "rate" in data["info"]:
            return float(data["info"]["rate"])
        elif "rates" in data and to_currency in data["rates"]:
            return data["rates"][to_currency]
        else:
            logger.error(f"Invalid API response: {data}")
            return 0.0
    except requests.RequestException:
        return 0.0  # Без logger.error
    except ValueError:
        return 0.0  # Без logger.error

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