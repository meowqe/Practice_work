"""Корзина покупателя. Корзина — список словарей {name, price, quantity}."""


def add_to_cart(cart, product, quantity=1):
    """Добавляет товар в корзину (изменяет cart) и возвращает её.

    Raises:
        ValueError: quantity <= 0 или в корзине станет больше, чем есть на складе.
    """
    if quantity <= 0:
        raise ValueError("Количество должно быть положительным")

    in_cart = next((i for i in cart if i["name"] == product["name"]), None)
    already = in_cart["quantity"] if in_cart else 0
    stock = product.get("quantity", 0)
    if already + quantity > stock:
        raise ValueError(
            f"Недостаточно товара '{product['name']}': на складе {stock}, в корзине уже {already}"
        )

    if in_cart:
        in_cart["quantity"] += quantity
    else:
        cart.append({"name": product["name"], "price": product["price"], "quantity": quantity})
    return cart


def remove_from_cart(cart, name):
    """Удаляет позицию из корзины по названию и возвращает корзину.

    Raises:
        KeyError: позиции с таким названием нет в корзине.
    """
    for index, item in enumerate(cart):
        if item["name"].lower() == str(name).strip().lower():
            del cart[index]
            return cart
    raise KeyError(f"В корзине нет товара '{name}'")


def clear_cart(cart):
    """Очищает корзину и возвращает её."""
    cart.clear()
    return cart


def cart_total(cart):
    """Возвращает сумму корзины с учётом количества каждой позиции."""
    return sum(item["price"] * item.get("quantity", 1) for item in cart)


def total_sum(products):
    """Возвращает суммарную стоимость списка товаров с учётом количества."""
    return sum(p["price"] * p["quantity"] for p in products)


def cart_count(cart):
    """Возвращает общее число единиц товара в корзине."""
    return sum(item.get("quantity", 1) for item in cart)
