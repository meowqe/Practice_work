"""Работа с каталогом товаров."""


def total_stock(product):
    """Суммарный остаток товара по всем размерам."""
    return sum(product["sizes"].values())


def get_low_stock(products, threshold=5):
    """Товары, суммарный остаток которых не больше threshold."""
    return [p for p in products if total_stock(p) <= threshold]


def search_advanced(products, query, category=None, min_price=None, max_price=None):
    q = query.lower().strip()
    result = []
    for p in products:
        if q and q not in p["name"].lower():
            continue
        if category and p["category"].lower() != category.lower():
            continue
        if min_price is not None and p["price"] < min_price:
            continue
        if max_price is not None and p["price"] > max_price:
            continue
        result.append(p)
    return result


def count_by_category(products):
    counts = {}
    for p in products:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    return counts


def avg_price(products):
    if not products:
        return 0.0
    return round(sum(p["price"] for p in products) / len(products), 2)
