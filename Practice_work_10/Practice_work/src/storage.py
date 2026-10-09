"""Хранение данных магазина «СпортТовары» в JSON-файлах."""
import json
import os


def save_json(data, filename):
    """Сохраняет данные в JSON-файл (UTF-8, с отступами). Создаёт папку при необходимости."""
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return filename


def load_json(filename, default=None):
    """Читает JSON-файл. Если файла нет, возвращает default.

    Raises:
        ValueError: файл существует, но содержит некорректный JSON.
    """
    if not os.path.exists(filename):
        return default
    with open(filename, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(f"Некорректный JSON в файле {filename}: {error}") from error


def save_orders(orders, filename="orders.json"):
    """Сохраняет список заказов в JSON-файл и возвращает имя файла."""
    return save_json(orders, filename)


def load_orders(filename="orders.json"):
    """Загружает список заказов. Если файла нет, возвращает пустой список."""
    return load_json(filename, default=[])


def save_products(products, filename):
    """Сохраняет каталог товаров в JSON-файл."""
    return save_json(products, filename)


def load_products(filename):
    """Загружает каталог товаров.

    Raises:
        FileNotFoundError: файл каталога не найден.
        ValueError: некорректный JSON.
    """
    data = load_json(filename, default=None)
    if data is None:
        raise FileNotFoundError(f"Файл каталога не найден: {filename}")
    return data
