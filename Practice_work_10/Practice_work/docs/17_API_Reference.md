# Справочник API (17)

Публичные функции модулей `src/`. Всего описано функций: **27**.

Товар — словарь `{name, brand, category, price, quantity}`. Позиция корзины — `{name, price, quantity}`. Заказ — `{id, customer, items, discount, total, created_at, status}`.

## Содержание

- [`src/catalog.py` — Каталог](#srcpy-catalog)
- [`src/cart.py` — Корзина](#srcpy-cart)
- [`src/orders.py` — Заказы](#srcpy-orders)
- [`src/analytics.py` — Аналитика](#srcpy-analytics)
- [`src/storage.py` — Хранение данных](#srcpy-storage)


## `src/catalog.py` — Каталог <a id="srcpy-catalog"></a>

### `get_low_stock(products, threshold=3)`

Возвращает товары, у которых остаток не больше порога, от меньшего остатка к большему.

**Параметры:**
- `products` (list[dict]) — список товаров
- `threshold` (int, по умолчанию `3`) — максимальный остаток

**Возвращает:**
- `list[dict]` — товары с низким остатком (новый список)

**Пример:**
```python
low = get_low_stock(products)
for p in low:
    print(p['name'], p['quantity'])
# Гантели 5 кг 1
# Футбольный мяч 2
# Футбольные бутсы 3
```

**Исключения:** —

### `highlight_low_stock(products, threshold=3)`

Печатает в консоль товары с низким остатком.

**Параметры:**
- `products` (list[dict])
- `threshold` (int, по умолчанию `3`)

**Возвращает:**
- `None`

**Пример:**
```python
highlight_low_stock(products)
# Товары с низким остатком:
# Гантели 5 кг - остаток: 1
```

**Исключения:** —

### `search_advanced(products, query, category=None, min_price=None, max_price=None)`

Комбинированный поиск по названию или бренду, категории и диапазону цен. Регистр не важен; все условия объединяются через «и».

**Параметры:**
- `products` (list[dict])
- `query` (str) — часть названия или бренда; пустая строка — без фильтра по тексту
- `category` (str | None) — точное название категории
- `min_price` (float | None) — минимальная цена
- `max_price` (float | None) — максимальная цена

**Возвращает:**
- `list[dict]` — подходящие товары

**Пример:**
```python
res = search_advanced(products, 'adidas', min_price=2000, max_price=5000)
print([p['name'] for p in res])
# ['Футбольный мяч', 'Спортивная форма']
```

**Исключения:** —

### `find_by_name(products, name)`

Находит товар по точному названию без учёта регистра и пробелов по краям.

**Параметры:**
- `products` (list[dict])
- `name` (str) — название товара

**Возвращает:**
- `dict | None` — товар или `None`, если не найден

**Пример:**
```python
find_by_name(products, ' скакалка ')['price']   # 700
```

**Исключения:** —

### `sort_products(products, key="name", reverse=False)`

Возвращает новый список, отсортированный по полю.

**Параметры:**
- `products` (list[dict])
- `key` (str, по умолчанию `"name"`) — одно из `name`, `price`, `quantity`, `brand`, `category`
- `reverse` (bool, по умолчанию `False`) — порядок по убыванию

**Возвращает:**
- `list[dict]` — отсортированная копия

**Пример:**
```python
cheap_first = sort_products(products, 'price')
cheap_first[0]['name']   # 'Скакалка'
```

**Исключения:** `ValueError` — недопустимое поле `key`

### `format_product(product)`

Формирует строку описания товара для вывода в каталоге.

**Параметры:**
- `product` (dict)

**Возвращает:**
- `str`

**Пример:**
```python
format_product(products[5])
# 'Скакалка | Reebok | Инвентарь | 700 руб. | в наличии: 15'
```

**Исключения:** —


## `src/cart.py` — Корзина <a id="srcpy-cart"></a>

### `add_to_cart(cart, product, quantity=1)`

Добавляет товар в корзину; если он уже есть, увеличивает количество. Проверяет остаток на складе.

**Параметры:**
- `cart` (list[dict]) — корзина (изменяется на месте)
- `product` (dict) — товар из каталога
- `quantity` (int, по умолчанию `1`) — сколько добавить

**Возвращает:**
- `list[dict]` — та же корзина

**Пример:**
```python
cart = []
add_to_cart(cart, products[5], 2)
# [{'name': 'Скакалка', 'price': 700, 'quantity': 2}]
```

**Исключения:** `ValueError` — `quantity <= 0` или суммарное количество в корзине больше остатка

### `remove_from_cart(cart, name)`

Удаляет позицию из корзины по названию (без учёта регистра).

**Параметры:**
- `cart` (list[dict])
- `name` (str)

**Возвращает:**
- `list[dict]` — та же корзина

**Пример:**
```python
remove_from_cart(cart, 'скакалка')   # []
```

**Исключения:** `KeyError` — такой позиции нет в корзине

### `clear_cart(cart)`

Полностью очищает корзину.

**Параметры:**
- `cart` (list[dict])

**Возвращает:**
- `list[dict]` — пустая корзина

**Пример:**
```python
clear_cart(cart)   # []
```

**Исключения:** —

### `cart_total(cart)`

Считает сумму корзины с учётом количества каждой позиции. Исправлено в `hotfix/cart-total`: раньше количество игнорировалось.

**Параметры:**
- `cart` (list[dict]) — позиции с полями `price` и `quantity` (если `quantity` нет, считается 1)

**Возвращает:**
- `int | float` — сумма в рублях

**Пример:**
```python
cart_total([{'price': 100, 'quantity': 2}, {'price': 50}])   # 250
```

**Исключения:** —

### `total_sum(products)`

Считает суммарную стоимость списка товаров (цена × количество).

**Параметры:**
- `products` (list[dict]) — у каждого есть `price` и `quantity`

**Возвращает:**
- `int | float`

**Пример:**
```python
total_sum([{'price': 100, 'quantity': 2}])   # 200
```

**Исключения:** `KeyError` — у товара нет `price` или `quantity`

### `cart_count(cart)`

Возвращает общее число единиц товара в корзине.

**Параметры:**
- `cart` (list[dict])

**Возвращает:**
- `int`

**Пример:**
```python
cart_count([{'quantity': 2}, {'quantity': 3}])   # 5
```

**Исключения:** —


## `src/orders.py` — Заказы <a id="srcpy-orders"></a>

### `apply_discount(total, percent)`

Применяет процентную скидку к сумме.

**Параметры:**
- `total` (int | float) — сумма
- `percent` (int | float) — скидка от 0 до 100

**Возвращает:**
- `int | float` — сумма после скидки, округлённая до копеек

**Пример:**
```python
apply_discount(1000, 10)   # 900
```

**Исключения:** `ValueError` — `percent` вне диапазона 0–100

### `reduce_stock(products, cart)`

Списывает со склада товары из корзины. Операция атомарна: при ошибке остатки не меняются.

**Параметры:**
- `products` (list[dict]) — каталог (изменяется на месте)
- `cart` (list[dict])

**Возвращает:**
- `list[dict]` — тот же каталог

**Пример:**
```python
reduce_stock(products, [{'name': 'Скакалка', 'price': 700, 'quantity': 2}])
products[5]['quantity']   # 13
```

**Исключения:** `ValueError` — товара нет в каталоге или его не хватает

### `create_order(cart, customer, discount=0, order_id=1, created_at=None)`

Создаёт заказ из корзины.

**Параметры:**
- `cart` (list[dict])
- `customer` (str) — имя покупателя
- `discount` (int | float, по умолчанию `0`) — скидка, %
- `order_id` (int, по умолчанию `1`)
- `created_at` (str | None) — время `ГГГГ-ММ-ДД ЧЧ:ММ:СС`; по умолчанию текущее

**Возвращает:**
- `dict` — заказ с полями `id`, `customer`, `items`, `discount`, `total`, `created_at`, `status`

**Пример:**
```python
order = create_order([{'name': 'Мяч', 'price': 100, 'quantity': 2}], 'Иван', discount=10)
order['total']   # 180
```

**Исключения:** `ValueError` — корзина пуста, не указан покупатель или некорректная скидка

### `next_order_id(orders)`

Возвращает номер для нового заказа.

**Параметры:**
- `orders` (list[dict])

**Возвращает:**
- `int` — максимальный номер + 1 (или `1` для пустого списка)

**Пример:**
```python
next_order_id([{'id': 3}, {'id': 1}])   # 4
```

**Исключения:** —


## `src/analytics.py` — Аналитика <a id="srcpy-analytics"></a>

### `count_by_category(products)`

Считает количество товаров в каждой категории.

**Параметры:**
- `products` (list[dict])

**Возвращает:**
- `dict[str, int]`

**Пример:**
```python
count_by_category(products)
# {'Мячи': 2, 'Обувь': 2, 'Одежда': 1, 'Инвентарь': 2, 'Аксессуары': 1}
```

**Исключения:** —

### `average_price(products)`

Средняя цена товара.

**Параметры:**
- `products` (list[dict])

**Возвращает:**
- `float` — средняя цена, `0.0` для пустого каталога

**Пример:**
```python
average_price(products)   # 3887.5
```

**Исключения:** —

### `stock_value(products)`

Стоимость всех остатков на складе (цена × количество).

**Параметры:**
- `products` (list[dict])

**Возвращает:**
- `int | float`

**Пример:**
```python
stock_value(products)   # 178300 для исходного каталога
```

**Исключения:** —

### `total_revenue(orders)`

Общая выручка по заказам.

**Параметры:**
- `orders` (list[dict])

**Возвращает:**
- `float`

**Пример:**
```python
total_revenue([{'total': 250.5}, {'total': 100}])   # 350.5
```

**Исключения:** —

### `top_products(orders, n=3)`

Самые продаваемые товары.

**Параметры:**
- `orders` (list[dict])
- `n` (int, по умолчанию `3`) — сколько товаров вернуть

**Возвращает:**
- `list[tuple[str, int]]` — пары (название, продано штук) по убыванию

**Пример:**
```python
top_products(orders, 1)   # [('Футбольный мяч', 2)]
```

**Исключения:** —


## `src/storage.py` — Хранение данных <a id="srcpy-storage"></a>

### `save_json(data, filename)`

Записывает данные в JSON (UTF-8, кириллица без экранирования). Создаёт недостающие папки.

**Параметры:**
- `data` — любые данные, сериализуемые в JSON
- `filename` (str)

**Возвращает:**
- `str` — имя файла

**Пример:**
```python
save_json({'a': 1}, 'data/test.json')
```

**Исключения:** `OSError` — не удалось записать файл

### `load_json(filename, default=None)`

Читает JSON-файл.

**Параметры:**
- `filename` (str)
- `default` — значение, если файла нет

**Возвращает:**
- данные из файла или `default`

**Пример:**
```python
load_json('data/cart.json', default=[])
```

**Исключения:** `ValueError` — файл содержит некорректный JSON

### `save_orders(orders, filename="orders.json")`

Сохраняет список заказов в JSON-файл.

**Параметры:**
- `orders` (list[dict])
- `filename` (str, по умолчанию `"orders.json"`)

**Возвращает:**
- `str` — имя файла

**Пример:**
```python
save_orders(orders, 'data/orders.json')
```

**Исключения:** —

### `load_orders(filename="orders.json")`

Загружает заказы из файла.

**Параметры:**
- `filename` (str, по умолчанию `"orders.json"`)

**Возвращает:**
- `list[dict]` — заказы или пустой список, если файла нет

**Пример:**
```python
orders = load_orders('data/orders.json')
```

**Исключения:** `ValueError` — некорректный JSON

### `save_products(products, filename)`

Сохраняет каталог в JSON-файл.

**Параметры:**
- `products` (list[dict])
- `filename` (str)

**Возвращает:**
- `str`

**Пример:**
```python
save_products(products, 'data/products.json')
```

**Исключения:** —

### `load_products(filename)`

Загружает каталог товаров.

**Параметры:**
- `filename` (str)

**Возвращает:**
- `list[dict]`

**Пример:**
```python
products = load_products('data/products.json')
```

**Исключения:** `FileNotFoundError` — файла нет; `ValueError` — некорректный JSON
