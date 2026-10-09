"""Оформление заказов."""
from datetime import datetime

from src.cart import cart_total


def apply_discount(total, percent):
    """Возвращает сумму после скидки percent (0–100), округлённую до копеек.

    Raises:
        ValueError: percent вне диапазона 0–100.
    """
    if not 0 <= percent <= 100:
        raise ValueError("Скидка должна быть от 0 до 100 процентов")
    result = round(total * (1 - percent / 100), 2)
    return int(result) if result == int(result) else result


def reduce_stock(products, cart):
    """Уменьшает остатки на складе по содержимому корзины (изменяет products).

    Raises:
        ValueError: товара нет в каталоге или его не хватает. При ошибке остатки не меняются.
    """
    by_name = {p["name"]: p for p in products}
    for item in cart:
        product = by_name.get(item["name"])
        if product is None:
            raise ValueError(f"Товара '{item['name']}' нет в каталоге")
        if product["quantity"] < item["quantity"]:
            raise ValueError(f"Недостаточно товара '{item['name']}' на складе")
    for item in cart:
        by_name[item["name"]]["quantity"] -= item["quantity"]
    return products


def create_order(cart, customer, discount=0, order_id=1, created_at=None):
    """Создаёт заказ из корзины и возвращает его как словарь.

    Raises:
        ValueError: корзина пуста, не указан покупатель или некорректна скидка.
    """
    if not cart:
        raise ValueError("Корзина пуста")
    if not str(customer).strip():
        raise ValueError("Не указан покупатель")

    total = apply_discount(cart_total(cart), discount)
    return {
        "id": order_id,
        "customer": str(customer).strip(),
        "items": [dict(item) for item in cart],
        "discount": discount,
        "total": total,
        "created_at": created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "new",
    }


def next_order_id(orders):
    """Возвращает номер для нового заказа (максимальный + 1, для пустого списка — 1)."""
    return max((o["id"] for o in orders), default=0) + 1
