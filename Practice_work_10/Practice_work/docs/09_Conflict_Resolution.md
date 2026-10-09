# Разрешение конфликта слияния

## Ситуация

От `develop` были созданы две ветки, в которых добавлена функция `total_sum` в конец `shop.py`:

| Ветка | Реализация |
|-------|-----------|
| `feature/total-v1` | `sum(p["price"] for p in products)` — без учёта количества |
| `feature/total-v2` | `sum(p["price"] * p["quantity"] for p in products)` — с учётом количества |

## Ход работы

1. Создал обе ветки от `develop`, в каждой сделал по коммиту.
2. Слил `feature/total-v1` в `develop` — слияние прошло без ошибок:
   ```
   git checkout develop
   git merge --no-ff feature/total-v1
   ```
3. Попробовал слить `feature/total-v2`:
   ```
   git merge feature/total-v2
   ```
   Результат:
   ```
   Auto-merging shop.py
   CONFLICT (content): Merge conflict in shop.py
   Automatic merge failed; fix conflicts and then commit the result.
   ```
   `git status` показал `UU shop.py` (изменён с обеих сторон).
4. В `shop.py` появились маркеры конфликта:
   ```
   def total_sum(products):
   <<<<<<< HEAD
       return sum(p["price"] for p in products)
   =======
       return sum(p["price"] * p["quantity"] for p in products)
   >>>>>>> feature/total-v2
   ```
   - между `<<<<<<< HEAD` и `=======` — версия из `develop` (v1);
   - между `=======` и `>>>>>>> feature/total-v2` — версия из сливаемой ветки (v2).
5. Выбрал версию v2: сумма заказа должна учитывать количество каждого товара. Удалил маркеры и вариант v1.
6. Проверил, что маркеров не осталось, и запустил функцию:
   `total_sum([{"price": 100, "quantity": 2}, {"price": 50, "quantity": 3}])` → `350` (100·2 + 50·3).
7. Завершил слияние:
   ```
   git add shop.py
   git commit -m "Разрешён конфликт в total_sum"
   ```
8. Удалил ветки `feature/total-v1` и `feature/total-v2` и отправил `develop` в удалённый репозиторий.

## Итоговый код

```python
def total_sum(products):
    return sum(p["price"] * p["quantity"] for p in products)
```

## Вывод

Конфликт возникает, когда две ветки меняют один и тот же участок файла. Git не знает, какая версия верна, поэтому решение принимает разработчик: выбирает нужный вариант (или объединяет оба), удаляет маркеры `<<<<<<<`, `=======`, `>>>>>>>` и делает коммит слияния.
