# Отчёт о тестировании

Команда: `python -m unittest discover -s tests`

## Итоги
| Показатель | Значение |
|---|---|
| Написано тестов | 37 |
| Прошло успешно (после исправления) | 37 |
| Упало при первом запуске | 3 |

## Тесты по функциям
| Функция | Тестов |
|---|---|
| `get_low_stock` | 7 |
| `highlight_low_stock` | 2 |
| `search_advanced` | 7 |
| `count_by_category` | 3 |
| `save_orders` | 1 |
| `total_sum` | 2 |
| `add_to_cart` | 7 (включая `test_invalid_size` и `test_division_by_zero` из задания) |
| `remove_from_cart` | 2 |
| `update_quantity` | 3 |
| `cart_total` | 3 |

## Найденные и исправленные ошибки
**Ошибка:** `get_low_stock` учитывала только поле `quantity` и игнорировала `sizes`.
**Упавшие тесты:** `test_no_low_stock`, `test_one_low_stock`, `test_sizes_are_summed`
(`AssertionError: 2 != 1`, `['A', 'B'] != ['A']`).
**Исправление:** функция `get_total_quantity` (сумма по `sizes`, иначе `quantity`), см. `13_Debugging.md`.

## Дополнение к shop.py
В исходном `shop.py` не было функций корзины, которые требует задание (`total_sum`, `cart_total`, `add_to_cart`, `remove_from_cart`, `update_quantity`). Они добавлены в раздел «Корзина»; остальной код файла не менялся.

## Функции без тестов
- Блок `if __name__ == "__main__"` — демонстрационный запуск, не функция; его работа проверена вручную.
