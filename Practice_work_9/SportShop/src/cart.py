"""Корзина покупок."""
from src.catalog import get_low_stock


def _find_product(products, product_id):
    for p in products:
        if p["id"] == product_id:
            return p
    return None


def _find_item(cart, product_id, size):
    for item in cart:
        if item["product_id"] == product_id and item["size"] == size:
            return item
    return None


def add_to_cart(cart, products, product_id, size, quantity):
    """Добавляет товар в корзину. Возвращает (успех, сообщение)."""
    if quantity <= 0:
        return False, "Количество должно быть положительным"
    product = _find_product(products, product_id)
    if product is None:
        return False, "Товар не найден"
    stock = product["sizes"].get(str(size))
    if stock is None:
        return False, "Такого размера нет"
    item = _find_item(cart, product_id, size)
    new_qty = (item["quantity"] if item else 0) + quantity
    if new_qty > stock:
        return False, f"Недостаточно на складе (доступно: {stock})"
    if item:
        item["quantity"] = new_qty
    else:
        cart.append({
            "product_id": product_id,
            "name": product["name"],
            "size": size,
            "quantity": quantity,
            "price": product["price"],
        })
    msg = "Товар добавлен в корзину"
    if product in get_low_stock(products):
        msg += " (внимание: остаток товара мал)"
    return True, msg


def remove_from_cart(cart, product_id, size):
    item = _find_item(cart, product_id, size)
    if item is None:
        return False, "Позиции нет в корзине"
    cart.remove(item)
    return True, "Позиция удалена"


def update_quantity(cart, products, product_id, size, new_qty):
    item = _find_item(cart, product_id, size)
    if item is None:
        return False, "Позиции нет в корзине"
    if new_qty <= 0:
        return remove_from_cart(cart, product_id, size)
    product = _find_product(products, product_id)
    stock = product["sizes"].get(str(size), 0)
    if new_qty > stock:
        return False, f"Недостаточно на складе (доступно: {stock})"
    item["quantity"] = new_qty
    return True, "Количество обновлено"


def cart_total(cart):
    return round(sum(i["price"] * i["quantity"] for i in cart), 2)
