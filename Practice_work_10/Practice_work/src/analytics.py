"""Аналитика по каталогу и заказам."""
from collections import Counter


def count_by_category(products):
    """Возвращает словарь {категория: количество товаров}."""
    categories = {}
    for product in products:
        category = product.get("category", "Без категории")
        categories[category] = categories.get(category, 0) + 1
    return categories


def average_price(products):
    """Возвращает среднюю цену товара (0.0 для пустого каталога)."""
    if not products:
        return 0.0
    return round(sum(p.get("price", 0) for p in products) / len(products), 2)


def stock_value(products):
    """Возвращает стоимость всех остатков на складе (цена × количество)."""
    return sum(p.get("price", 0) * p.get("quantity", 0) for p in products)


def total_revenue(orders):
    """Возвращает общую выручку по списку заказов."""
    return round(sum(order.get("total", 0) for order in orders), 2)


def top_products(orders, n=3):
    """Возвращает n самых продаваемых товаров: список (название, продано штук)."""
    sold = Counter()
    for order in orders:
        for item in order.get("items", []):
            sold[item["name"]] += item["quantity"]
    return sold.most_common(n)
