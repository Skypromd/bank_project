# src/decorators.py
import logging
from datetime import datetime
from functools import wraps
from typing import Optional


def log(filename: Optional[str] = None):
    """
    Декоратор для логирования вызовов функции.

    :param filename: Имя файла для логирования. Если не указано, логирование в консоль.
    :return: Декорированная функция.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)
            logger.handlers.clear()

            if filename:
                handler = logging.FileHandler(filename)
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                logger.info(
                    f"Function {func.__name__} executed successfully with result: {result}"
                )
                return result
            except Exception as e:
                logger.error(f"Function {func.__name__} failed with error: {str(e)}")
                raise
            finally:
                end_time = datetime.now()
                execution_time = (end_time - start_time).total_seconds()
                logger.info(f"Execution time: {execution_time} seconds")
                if handler in logger.handlers:
                    handler.close()
                    logger.removeHandler(handler)

        return wrapper

    return decorator
