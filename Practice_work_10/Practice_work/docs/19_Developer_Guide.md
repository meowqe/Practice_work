# Руководство разработчика (19)

## 1. Настройка окружения

Нужны Python 3.10+ и Git. Внешних библиотек нет, `pip install` не требуется.

```bash
git clone <URL репозитория>
cd my_os
python --version          # 3.10 или выше
python main.py --version  # СпортТовары 1.0
```

Рекомендуется VS Code с расширением Python. Папки `.venv/`, `.vscode/`, `dist/` и рабочие файлы `data/cart.json`, `data/orders.json` исключены из Git (`.gitignore`).

## 2. Устройство проекта

| Модуль | Ответственность |
|--------|-----------------|
| `src/catalog.py` | поиск, сортировка, остатки |
| `src/cart.py` | корзина |
| `src/orders.py` | заказы, скидки, списание со склада |
| `src/analytics.py` | аналитика |
| `src/storage.py` | JSON-файлы |
| `main.py` | разбор команд и вывод, бизнес-логики нет |

Правило: вся логика живёт в `src/` и не печатает ничего (кроме `highlight_low_stock`), а `main.py` только вызывает её и форматирует вывод. Так функции легко тестировать.

## 3. Запуск тестов

```bash
python -m unittest discover -s tests          # все тесты
python -m unittest tests.test_cart            # один модуль
python -m unittest tests.test_cart -v         # подробный вывод
```

Тесты работают с временными папками и не трогают `data/`. Перед коммитом все тесты должны проходить.

## 4. Как добавить новую функцию

Пример: функция `get_by_brand(products, brand)`.

1. Создайте ветку от `develop` (см. раздел 5).
2. Напишите тест в `tests/test_catalog.py` (он должен сначала падать):
   ```python
   def test_get_by_brand(self):
       self.assertEqual(len(get_by_brand(PRODUCTS, "adidas")), 2)
   ```
3. Реализуйте функцию в подходящем модуле `src/` с docstring (назначение, параметры, исключения).
4. Если нужна команда в консоли, добавьте подкоманду в `build_parser()` и обработку в `run()` в `main.py`.
5. Запустите тесты.
6. Опишите функцию в `docs/17_API_Reference.md` по шаблону: назначение, параметры, возвращаемое значение, пример, исключения.
7. Сделайте коммит: `git commit -m "US-N: добавлена функция get_by_brand"`.

## 5. Ветки и Pull Request

Схема ветвления описана в [08_Git_Flow.md](08_Git_Flow.md): `main` (стабильная), `develop` (интеграция), `feature/*`, `hotfix/*`.

```bash
git checkout develop
git pull
git checkout -b feature/by-brand       # новая ветка от develop
# ... работа и коммиты ...
git push -u origin feature/by-brand
```

Затем откройте Pull Request `feature/by-brand → develop` и оформите описание по образцу [10_Pull_Request.md](10_Pull_Request.md): что сделано, как проверить, связанные задачи, ревьюер. После одобрения:

```bash
git checkout develop
git merge --no-ff feature/by-brand
git branch -d feature/by-brand
git push
```

Срочное исправление ошибки в `main` делается через `hotfix/*` от `main` и вливается и в `main`, и в `develop` ([11_Hotfix.md](11_Hotfix.md)). Если при слиянии возник конфликт, действуйте по [09_Conflict_Resolution.md](09_Conflict_Resolution.md).

## 6. Сборка

```bash
python build.py
```

Скрипт:
1. запускает все тесты; при ошибке сборка прерывается с кодом 1;
2. упаковывает `src/` (без модулей учебной ОС), `data/`, `docs/`, `main.py`, `README.md` в `dist/SportShop-1.0.zip`; рабочие `cart.json` и `orders.json` в архив не попадают.

Для нового релиза измените `VERSION` в `build.py` и `main.py`.

## 7. Релиз

```bash
git checkout main
git merge --no-ff develop
git tag -a v1.0 -m "Релиз версии 1.0"
git push origin main develop v1.0
```

Проверить тег в удалённом репозитории: `git ls-remote --tags origin`.
