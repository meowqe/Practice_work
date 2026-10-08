"""Аналитика по заказам."""


def total_revenue(orders):
    return round(sum(o["total"] for o in orders), 2)


def best_selling_product(orders):
    """Возвращает (название, количество) самого продаваемого товара или None."""
    sold = {}
    for o in orders:
        for i in o["items"]:
            sold[i["name"]] = sold.get(i["name"], 0) + i["quantity"]
    if not sold:
        return None
    name = max(sold, key=sold.get)
    return name, sold[name]


def average_order_total(orders):
    if not orders:
        return 0.0
    return round(total_revenue(orders) / len(orders), 2)
