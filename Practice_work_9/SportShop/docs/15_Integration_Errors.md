# Ошибки интеграции

## 1. Какая ошибка была внесена?

В модуле `src/cart.py` в функции `add_to_cart` изменён формат позиции корзины.
Вместо ключа `'name'` использован ключ `'product'`:

```python
cart.append({
    "product_id": product_id,
    "product": product["name"],   # было: "name": product["name"]
    "size": size,
    "quantity": quantity,
    "price": product["price"],
})
```

Модуль `src/orders.py` ожидает ключ `'name'` (`item["name"]`), то есть нарушено соглашение о формате данных на стыке модулей `cart` → `orders`.

## 2. Как она проявилась?

Интеграционные тесты (`python -m unittest tests.test_integration`) упали: `FAILED (errors=2)`.

```
ERROR: test_full_cycle (tests.test_integration.TestIntegration.test_full_cycle)
  File "tests/test_integration.py", line 27, in test_full_cycle
    order = create_order(self.cart, 'Тестовый клиент', self.products)
  File "src/orders.py", line 20, in create_order
    "name": item["name"],
KeyError: 'name'
```

Важное наблюдение: модульные тесты `test_cart.py` **не обнаружили** ошибку — они проверяют только сумму и остатки, но не структуру позиции. Ошибка находится именно на стыке модулей, и поймал её только интеграционный тест. Это показывает, почему интеграционное тестирование необходимо.
Третий интеграционный тест (`test_low_stock_warning_reaches_cart`) прошёл, так как не доходит до `create_order`.

## 3. Как была исправлена?

1. По traceback определено место падения — `orders.py:20`, ключ `'name'`.
2. Выяснено, что `orders.py` получает данные из `cart.py`, поэтому проверена структура позиции в `add_to_cart`.
3. Ключ `'product'` возвращён к принятому формату `'name'`.
4. Повторный запуск: `Ran 14 tests ... OK`.

Вывод: формат данных, передаваемых между модулями (ключи словаря позиции корзины), — это «контракт»; его изменение должно сопровождаться изменением всех потребителей и тестов.
