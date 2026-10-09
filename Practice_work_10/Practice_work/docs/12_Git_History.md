# История Git

Команда: `git log --oneline --graph --all`

```
* 3bd2550 docs: описание hotfix (11)
*   af4a6b5 Merge hotfix/cart-total into develop (разрешён конфликт рядом с total_sum)
|\  
| | *   c76b793 Merge hotfix/cart-total into main
| | |\  
| | |/  
| |/|   
| * | d65f180 hotfix: cart_total теперь учитывает количество товара
| |/  
| | * 8db633d docs: описание Pull Request (10)
| | * a9afd2d US-2: добавлена функция search_advanced и тесты
| |/  
|/|   
* | f3646ee docs: описание разрешения конфликта (09)
* |   c9ab28b Разрешён конфликт в total_sum
|\ \  
| * | c8cc0fc US-3: добавлена total_sum (версия 2, с учётом количества)
* | |   c09b985 Merge feature/total-v1 into develop
|\ \ \  
| |/ /  
|/| |   
| * | fa03515 US-3: добавлена total_sum (версия 1, без учёта количества)
|/ /  
* |   4897ec3 Merge feature/low-stock into develop
|\ \  
| * | 1b43132 US-1: добавлена функция get_low_stock
|/ /  
* / 2bec179 docs: схема Git Flow (08)
|/  
* 1d33ee7 Добавлен shop.py: count_by_category, save_orders, cart_total
* cc9a8d0 docs: требования и NFR
* f280ddb Каркас MyOS: ядро, shell, БД, тесты
```

## Анализ графа

**Сколько веток было создано?**
Шесть: `develop`, `feature/low-stock`, `feature/total-v1`, `feature/total-v2`, `hotfix/cart-total` и `feature/search-advanced` (плюс исходная `main`). Вспомогательные ветки, кроме `feature/search-advanced`, удалены после слияния. `feature/search-advanced` оставлена открытой: это Pull Request, который ждёт ревью.

**Какие слияния произошли?**
1. `feature/low-stock` → `develop`
2. `feature/total-v1` → `develop`
3. `feature/total-v2` → `develop` (с конфликтом)
4. `hotfix/cart-total` → `main`
5. `hotfix/cart-total` → `develop` (с конфликтом)

Слияния выполнялись с `--no-ff`, чтобы каждое из них было видно на графе отдельным коммитом.

**Был ли конфликт и как он разрешён?**
Было два конфликта, оба в `shop.py`:
- `total_sum` (v1 против v2): оставлена версия v2 с учётом количества, коммит «Разрешён конфликт в total_sum».
- `cart_total` при слиянии hotfix в `develop`: оставлены исправленный `cart_total` и `total_sum` из `develop`.

Подробности в `09_Conflict_Resolution.md` и `11_Hotfix.md`.
