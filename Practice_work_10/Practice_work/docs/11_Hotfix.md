# Hotfix: cart_total

## Проблема

В `main` обнаружена критическая ошибка: функция `cart_total` возвращала неверную сумму, потому что суммировала только цены и не учитывала количество товара:

```python
return sum(item["price"] for item in cart)   # было
```

Корзина из 2 штук товара за 100 и 1 штуки за 50 давала 150 вместо 250.

## Процесс

1. Создал ветку от `main` (а не от `develop`: в `develop` лежит ещё не выпущенный код):
   ```
   git checkout main
   git checkout -b hotfix/cart-total
   ```
2. Исправил функцию и сделал коммит:
   ```python
   return sum(item["price"] * item.get("quantity", 1) for item in cart)
   ```
   ```
   git commit -m "hotfix: cart_total теперь учитывает количество товара"
   ```
3. Слил hotfix в `main`:
   ```
   git checkout main
   git merge --no-ff hotfix/cart-total
   ```
4. Слил hotfix в `develop`, чтобы исправление не потерялось при следующем релизе:
   ```
   git checkout develop
   git merge --no-ff hotfix/cart-total
   ```
   Здесь возник конфликт: в `develop` сразу под `cart_total` была добавлена `total_sum`, и правки оказались в соседних строках. Разрешил, оставив исправленный `cart_total` из hotfix и `total_sum` из `develop`, затем `git add shop.py && git commit`.
5. Проверил результат: `cart_total([{"price": 100, "quantity": 2}, {"price": 50}])` → `250`.
6. Удалил ветку и отправил изменения:
   ```
   git branch -d hotfix/cart-total
   git push origin main develop
   ```

## Вывод

Hotfix создаётся от `main` и вливается и в `main`, и в `develop`. Если забыть `develop`, ошибка вернётся со следующим релизом.
