import json


def get_low_stock(products):
    """
    Возвращает товары, у которых суммарное количество <= 3.
    """
    low_stock = []

    for product in products:
        quantity = product.get("quantity", 0)

        if quantity <= 3:
            low_stock.append(product)

    return sorted(low_stock, key=lambda product: product.get("quantity", 0))


def highlight_low_stock(products):
    """
    Выводит товары с низким остатком.
    """
    low_stock = get_low_stock(products)

    if not low_stock:
        print("Нет товаров с низким остатком")
        return

    print("Товары с низким остатком:")

    for product in low_stock:
        print(
            f"{product.get('name', 'Без названия')} - "
            f"остаток: {product.get('quantity', 0)}"
        )


def count_by_category(products):
    """
    Возвращает словарь:
    {категория: количество товаров}
    """
    categories = {}

    for product in products:
        category = product.get("category", "Без категории")

        if category not in categories:
            categories[category] = 0

        categories[category] += 1

    return categories


def save_orders(orders, filename="orders.json"):
    """
    Сохраняет список заказов в JSON-файл.
    """
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=4)

    print(f"Заказы сохранены в файл {filename}")


def cart_total(cart):
    """
    Возвращает общую сумму корзины.
    """
    return sum(item["price"] * item.get("quantity", 1) for item in cart)


def total_sum(products):
    return sum(p["price"] * p["quantity"] for p in products)
