"""Оформление и хранение заказов."""
import os
from datetime import datetime

from src.cart import cart_total
from src.storage import read_json, write_json


def create_order(cart, client_name, products):
    """Создаёт заказ из корзины. Возвращает dict или None."""
    if not cart or not client_name.strip():
        return None
    known_ids = {p["id"] for p in products}
    items = []
    for item in cart:
        if item["product_id"] not in known_ids:
            return None
        items.append({
            "product_id": item["product_id"],
            "name": item["name"],
            "size": item["size"],
            "quantity": item["quantity"],
            "price": item["price"],
        })
    return {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "date": datetime.now().isoformat(timespec="seconds"),
        "client": client_name.strip(),
        "items": items,
        "total": cart_total(cart),
    }


def print_order(order):
    print(f"Заказ №{order['id']} от {order['date']}")
    print(f"Клиент: {order['client']}")
    for i in order["items"]:
        print(f"  {i['name']} (р. {i['size']}) x{i['quantity']} = {i['price'] * i['quantity']:.2f} руб.")
    print(f"ИТОГО: {order['total']:.2f} руб.")


def save_orders(orders, filename):
    write_json(orders, filename)


def load_orders(filename):
    if not os.path.exists(filename):
        return []
    return read_json(filename)
