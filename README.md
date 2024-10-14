## Проект: Виджет банковских операций

## Описание
Этот проект предназначен для обработки данных о банковских операциях. Он включает функции для фильтрации операций по состоянию и сортировки операций по дате.

## Цели проекта
- Обеспечить удобный интерфейс для работы с банковскими операциями.
- Позволить пользователям фильтровать и сортировать операции.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Skypromd/bank_project.gitRL
## Модуль generators

### Функции

- **filter_by_currency(transactions, currency)**: Возвращает итератор транзакций по заданной валюте.
  
  **Пример использования**:
  ```python
  usd_transactions = filter_by_currency(transactions, "USD")
  for _ in range(2):
      print(next(usd_transactions))



## Тестирование

- Для запуска тестов используйте `pytest`. Убедитесь, что у вас установлены все зависимости, и выполните команду:

```bash
pytest

###  4: Проверка покрытия тестами

 1. **Установите необходимые зависимости**:
   Убедитесь, что у вас установлены `pytest` и `pytest-cov` для проверки покрытия кода:

   ```bash
   pip install pytest pytest-cov