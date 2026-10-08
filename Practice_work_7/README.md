# MyOS — учебная операционная система

Учебная ОС с монолитным ядром на Python 3.10+ и SQLite (без внешних зависимостей).

## Запуск
```
python src/db.py        # создать БД db/os.sqlite
python -m src.shell     # командная оболочка
python -m unittest discover -s tests -t .   # тесты
```
Учётные записи по умолчанию (учебные): `admin / admin123`, `user / user123`.

## Структура
`src/` — код (kernel, syscalls, shell, db, config, logger) · `docs/` — документация · `db/` — база · `tests/` — тесты · `logs/` — журналы.

Проектная документация: [docs/01_OS_Scope_and_NFR.md](docs/01_OS_Scope_and_NFR.md)
