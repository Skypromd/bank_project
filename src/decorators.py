# src/decorators.py
import functools
import logging
import sys
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования работы функции."""
    if filename:
        logging.basicConfig(filename=filename, level=logging.INFO, format="%(asctime)s - %(message)s")
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s - %(message)s")

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                logging.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                logging.error(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise

        return wrapper

    return decorator
