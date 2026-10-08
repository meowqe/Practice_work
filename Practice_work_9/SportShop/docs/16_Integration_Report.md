# Отчёт об интеграции модулей (Практическое занятие №9)

## 1. Выделенные модули

| Модуль | Назначение | Функции |
|---|---|---|
| `src/storage.py` | Работа с JSON | `load_products`, `save_products` (+ общие `read_json`, `write_json`) |
| `src/catalog.py` | Каталог | `get_low_stock`, `search_advanced`, `count_by_category`, `avg_price` |
| `src/cart.py` | Корзина | `add_to_cart`, `remove_from_cart`, `update_quantity`, `cart_total` |
| `src/orders.py` | Заказы | `create_order`, `print_order`, `save_orders`, `load_orders` |
| `src/analytics.py` | Аналитика | `total_revenue`, `best_selling_product`, `average_order_total` |

Порядок интеграции — **восходящий (bottom-up)**: storage/catalog → cart → orders → analytics → main.py.

## 2. Используемые импорты

- `cart.py`: `from src.catalog import get_low_stock` (предупреждение о малом остатке при добавлении в корзину)
- `orders.py`: `from src.cart import cart_total`, `from src.storage import read_json, write_json`
- `analytics.py`: зависимостей от других модулей нет (работает с готовыми заказами)
- `main.py`: функции из `catalog`, `cart`, `orders`, `analytics`, `storage`
- Тесты: `from src.<модуль> import ...`; запуск из корня проекта.

Зависимости направлены строго «вверх» (без циклических импортов):
`storage ← orders`, `catalog ← cart ← orders`, `analytics` — независим.

## 3. Интеграционные тесты (`tests/test_integration.py`)

1. `test_full_cycle` — загрузка товаров → корзина → заказ → сохранение в JSON → загрузка → сравнение суммы.
2. `test_cart_to_analytics` — корзина с двумя позициями → заказ → JSON → `total_revenue`, `best_selling_product`.
3. `test_low_stock_warning_reaches_cart` — проверка связки `catalog.get_low_stock` → `cart.add_to_cart`.

Также написаны модульные тесты по каждому модулю (`test_catalog/cart/orders/analytics.py`). Всего 14 тестов.

## 4. Найденные и исправленные ошибки

Намеренно внесена ошибка формата данных (`'product'` вместо `'name'` в `cart.py`) — интеграционные тесты упали с `KeyError: 'name'`, ошибка исправлена. Подробности: `docs/15_Integration_Errors.md`.
Побочный вывод: модульные тесты корзины ошибку не заметили, она видна только на стыке модулей.

## 5. Скрипт сборки (`build.py`)

1. `check_python_version()` — требуется Python 3.10+.
2. `install_dependencies()` — ставит пакеты из `requirements.txt`, если файл есть (сейчас внешних зависимостей нет).
3. `check_data()` — проверка `data/products.json`.
4. `run_tests()` — `python -m unittest discover -s tests -v`; при падении сборка прерывается с кодом 1.
5. `run_app()` — запуск `main.py` после успешных тестов.

Запуск: `python build.py`.
