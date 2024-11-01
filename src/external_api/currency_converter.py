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

# Настройка логирования для отслеживания действий программы
logging.basicConfig(level=logging.INFO)

# Глобальный кэш для хранения предыдущих курсов валют
currency_cache = {}
cache_expiry_time = 3600  # 1 час, время жизни кэша


def get_conversion_rate(from_currency: str, to_currency: str) -> float:
    """
    Получает курс конвертации из кэша или API.

    :param from_currency: Код валюты, из которой конвертируем.
    :param to_currency: Код валюты, в которую конвертируем.
    :return: Курс конвертации.
    """
    global currency_cache

    cache_key = f"{from_currency}_{to_currency}"
    current_time = time.time()

    # Проверка наличия курса в кэше
    if cache_key in currency_cache:
        cached_rate, timestamp = currency_cache[cache_key]
        # Проверка, не истек ли срок действия кэша
        if current_time - timestamp < cache_expiry_time:
            return cached_rate  # Возвращаем кэшированный курс

    # Если кэш устарел или отсутствует, запрашиваем новый курс
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY не найдена в переменных окружения.")

    try:
        response = requests.get(
            API_URL,
            params={"from": from_currency, "to": to_currency},
            headers={"apikey": api_key}
        )
        response.raise_for_status()  # Проверка на ошибки запроса

        rate = response.json().get("info", {}).get("rate", 0.0)

        if rate <= 0:
            logging.error("Получен некорректный курс конвертации.")
            return 0.0

        # Сохраняем курс в кэш
        currency_cache[cache_key] = (rate, current_time)
        return rate
    except requests.RequestException as e:
        logging.error(f"Ошибка запроса к API: {e}")
        return 0.0
    except ValueError:
        logging.error("Ошибка при обработке ответа API.")
        return 0.0


def convert_currency(transaction_data: dict) -> float:
    """
    Конвертирует сумму транзакции из USD или EUR в рубли.

    :param transaction_data: Данные о транзакции.
    :return: Сумма в рублях (float).
    """
    logging.info(f"Получена транзакция: {transaction_data}")

    operation_amount = transaction_data.get("operationAmount")
    if operation_amount is None:
        logging.warning("Отсутствует 'operationAmount' в транзакции.")
        return 0.0

    amount_str = operation_amount.get("amount")
    if amount_str is None:
        logging.warning("Отсутствует 'amount' в 'operationAmount'.")
        return 0.0

    try:
        amount = float(amount_str)
        if amount < 0:
            logging.warning("Отрицательная сумма не может быть конвертирована.")
            return 0.0
    except ValueError:
        logging.error("Некорректное значение 'amount'.")
        return 0.0

    currency = operation_amount.get("currency", {}).get("code")
    if currency is None:
        logging.warning("Отсутствует код валюты.")
        return 0.0

    # Если валюта уже в рублях, возвращаем сумму
    if currency == "RUB":
        return amount

    # Поддерживаемые валюты для конвертации
    supported_currencies = ["USD", "EUR"]
    if currency in supported_currencies:
        # Получаем курс конвертации из кэша или API
        conversion_rate = get_conversion_rate(currency, "RUB")
        if conversion_rate <= 0:
            logging.error(f"Некорректный результат конвертации для {amount} {currency}.")
            return 0.0

        # Конвертируем сумму
        converted_amount = amount * conversion_rate
        logging.info(f"Конвертировано {amount} {currency} в {converted_amount:.2f} RUB.")
        return converted_amount

    logging.warning(f"Неизвестная валюта: {currency}.")
    return 0.0

def load_transactions_from_file(json_file_path: str) -> list:
    """
    Загружает транзакции из JSON-файла.

    :param json_file_path: Путь к JSON-файлу.
    :return: Список транзакций.
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

# Укажите путь к вашему JSON-файлу
file_path = '/home/mdgagauz/PycharmProjects/bank_project/data/operations.json'

# Загружаем транзакции
transactions = load_transactions_from_file(file_path)

# Обработка всех транзакций
for txn in transactions:
    result = convert_currency(txn)
    print(f"Транзакция ID {txn.get('id', 'неизвестен')} конвертирована в RUB: {result:.2f}")