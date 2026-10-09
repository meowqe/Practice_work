## PR: feature/search-advanced → develop

**Что сделано:**
- Добавлена функция `search_advanced(products, query, category=None, min_price=None, max_price=None)` в `shop.py`.
- Поиск идёт по названию и бренду (без учёта регистра), затем применяются фильтры по категории и диапазону цен. Все параметры, кроме `query`, необязательные.
- Добавлены unit-тесты в `tests/test_shop.py`.

**Как проверить:**
1. `git checkout feature/search-advanced`
2. `python -m unittest tests.test_shop` — все 3 теста должны пройти.
3. Вручную: `search_advanced(products, "adidas", min_price=2000, max_price=5000)` возвращает 2 товара (Футбольный мяч и Спортивная форма).

**Связанные задачи:** US-2

**Ревьюер:** <ФИО>
