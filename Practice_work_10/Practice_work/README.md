# СпортТовары — система управления магазином

## Описание

Консольное приложение на Python для небольшого магазина спортивных товаров. Умеет показывать каталог, искать товары по названию, бренду, категории и цене, вести корзину, оформлять заказы со скидкой, хранить заказы в JSON и показывать аналитику (выручка, топ товаров, остатки). Внешних зависимостей нет.

Версия: **1.0**

## Требования

- Python 3.10+
- Git
- SQLite не нужен: данные хранятся в JSON-файлах

## Установка

```bash
git clone <URL репозитория>
cd my_os        # папка проекта (в задании — SportShop)
```

## Запуск

```bash
python main.py --help
python main.py catalog
python main.py search adidas --min-price 2000 --max-price 5000
python main.py cart add "Скакалка" -q 2
python main.py checkout --customer "Иван Петров" --discount 10
python main.py analytics
```

Полный список сценариев с результатами — в [docs/18_User_Guide.md](docs/18_User_Guide.md).

## Тестирование

```bash
python -m unittest discover -s tests
```

## Сборка

```bash
python build.py
```

Скрипт сначала запускает тесты, затем создаёт архив `dist/SportShop-1.0.zip`.

## Структура проекта

```
my_os/
├── src/
│   ├── catalog.py      # каталог: поиск, сортировка, низкий остаток
│   ├── cart.py         # корзина
│   ├── orders.py       # заказы, скидки, списание со склада
│   ├── analytics.py    # аналитика
│   ├── storage.py      # чтение и запись JSON
│   └── (kernel.py, shell.py, db.py, ...)  # учебная ОС MyOS, практики 1–6
├── tests/              # unittest
├── docs/               # документация (01–21)
├── data/
│   └── products.json   # каталог товаров
├── main.py             # точка входа
├── build.py            # сборка релиза
├── shop.py             # слой совместимости с практикой №7
└── README.md
```

В репозитории также лежит учебная ОС MyOS из практик 1–6 (`src/kernel.py`, `src/shell.py` и др.); в релиз магазина она не входит. Описание ОС: [docs/01_OS_Scope_and_NFR.md](docs/01_OS_Scope_and_NFR.md).

## Документация

| Файл | Содержание |
|------|-----------|
| [docs/17_API_Reference.md](docs/17_API_Reference.md) | справочник функций |
| [docs/18_User_Guide.md](docs/18_User_Guide.md) | руководство пользователя |
| [docs/19_Developer_Guide.md](docs/19_Developer_Guide.md) | руководство разработчика |
| [docs/20_Final_Test_Report.md](docs/20_Final_Test_Report.md) | итоговое тестирование |
| [docs/21_Presentation.md](docs/21_Presentation.md) | презентация проекта |
| [docs/08_Git_Flow.md](docs/08_Git_Flow.md) | схема ветвления |

## Авторы

- <ФИО>, группа <группа>
