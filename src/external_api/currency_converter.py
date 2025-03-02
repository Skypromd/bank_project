import json
import os
import requests
from dotenv import load_dotenv
import logging
import time

# Загружаем переменные окружения из .env
load_dotenv()

# URL API для конвертации валют
API_URL = "https://api.apilayer.com/exchangerates_data/convert"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Глобальный кэш для хранения предыдущих курсов валют
currency_cache = {}
cache_expiry_time = 3600  # 1 час, время жизни кэша

def get_conversion_rate(from_currency: str, to_currency: str) -> float:
    """
    Получает курс конвертации из кэша или API.
    Обратите внимание: убедитесь, что API-ключ в .env файле корректный и действующий.
    """
    global currency_cache
    cache_key = f"{from_currency}_{to_currency}"
    current_time = time.time()

    # Проверка наличия курса в кэше
    if cache_key in currency_cache:
        cached_rate, timestamp = currency_cache[cache_key]
        if current_time - timestamp < cache_expiry_time:
            return cached_rate  # Возвращаем кэшированный курс

    # Если кэш устарел или отсутствует, запрашиваем новый курс
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY не найдена в переменных окружения.")

    try:
        response = requests.get(
            API_URL,
            params={"from": from_currency, "to": to_currency, "amount": 1},  # Запрашиваем курс за 1 единицу
            headers={"apikey": api_key}
        )
        response.raise_for_status()  # Проверка на ошибки запроса

        # Обработка ответа
        api_response = response.json()
        if 'info' in api_response and 'rate' in api_response['info']:
            rate = api_response['info']['rate']  # Получаем курс из поля 'info'
            if rate <= 0:
                logging.error("Получен некорректный курс конвертации.")
                return 0.0
            # Сохраняем курс в кэш
            currency_cache[cache_key] = (rate, current_time)
            return rate
        else:
            logging.error(f"Ошибка в ответе API: {api_response}")
            return 0.0

    except requests.RequestException as e:
        logging.error(f"Ошибка запроса к API: {e}, статус код: {e.response.status_code if e.response else 'нет ответа'}")
        return 0.0
    except ValueError:
        logging.error("Ошибка при обработке ответа API.")
        return 0.0

def convert_currency(transaction_data: dict) -> float:
    """
    Конвертирует сумму транзакции из USD или EUR в рубли.
    """
    logging.info(f"Получена транзакция: {transaction_data}")

    operation_amount = transaction_data.get("operationAmount")
    if operation_amount is None:
        logging.warning("Отсутствует 'operationAmount' в транзакции.")
        return 0.0

    amount_str = operation_amount.get("amount")
    try:
        amount = float(amount_str)
        if amount < 0:
            logging.warning("Отрицательная сумма не может быть конвертирована.")
            return 0.0
    except ValueError:
        logging.error("Некорректное значение 'amount'.")
        return 0.0

    currency_code = operation_amount.get("currency", {}).get("code")
    if currency_code is None:
        logging.warning("Отсутствует код валюты.")
        return 0.0

    # Если валюта уже в рублях, возвращаем сумму
    if currency_code == "RUB":
        return amount

    # Поддерживаемые валюты для конвертации
    supported_currencies = ["USD", "EUR"]
    if currency_code in supported_currencies:
        conversion_rate = get_conversion_rate(currency_code, "RUB")
        if conversion_rate <= 0:
            logging.error(f"Некорректный результат конвертации для {amount} {currency_code}.")
            return 0.0

        # Конвертируем сумму
        converted_amount = amount * conversion_rate
        logging.info(f"Конвертировано {amount} {currency_code} в {converted_amount:.2f} RUB.")
        return converted_amount

    logging.warning(f"Неизвестная валюта: {currency_code}.")
    return 0.0

def load_transactions_from_file(json_file_path: str) -> list:
    """
    Загружает транзакции из JSON-файла.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            loaded_transactions = json.load(file)
            logging.info(f"Загружено {len(loaded_transactions)} транзакций из файла {json_file_path}.")
            return loaded_transactions
    except FileNotFoundError:
        logging.error(f"Файл не найден: {json_file_path}")
        return []
    except json.JSONDecodeError:
        logging.error("Ошибка при декодировании JSON.")
        return []

def validate_transaction(txn):
    """
    Проверяет, что транзакция содержит необходимые поля.
    """
    required_fields = ['operationAmount', 'id']
    for field in required_fields:
        if field not in txn:
            logging.warning(f"Транзакция {txn} отсутствует поле: {field}")
            return False
    return True

if __name__ == '__main__':
    # Укажите путь к вашему JSON-файлу без пробелов
    file_path = '/home/mdgagauz/PycharmProjects/bank_project/data/operations.json'

    # Загружаем транзакции
    transactions = load_transactions_from_file(file_path)

    # Обработка всех транзакций
    for transaction_item in transactions:
        if validate_transaction(transaction_item):
            result = convert_currency(transaction_item)
            print(f"Транзакция ID {transaction_item.get('id', 'неизвестен')} конвертирована в RUB: {result:.2f}")