"""Сохранение и загрузка данных в формате JSON."""
import json
import os


def read_json(filename):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def write_json(data, filename):
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_products(filename):
    return read_json(filename)


def save_products(products, filename):
    write_json(products, filename)
