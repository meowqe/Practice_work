"""Каталог товаров: просмотр, поиск, сортировка, контроль остатков."""

SORT_KEYS = ("name", "price", "quantity", "brand", "category")


def get_low_stock(products, threshold=3):
    """Возвращает товары с количеством <= threshold, по возрастанию остатка."""
    low_stock = [p for p in products if p.get("quantity", 0) <= threshold]
    return sorted(low_stock, key=lambda product: product.get("quantity", 0))


def highlight_low_stock(products, threshold=3):
    """Выводит в консоль товары с низким остатком."""
    low_stock = get_low_stock(products, threshold)

    if not low_stock:
        print("Нет товаров с низким остатком")
        return

    print("Товары с низким остатком:")
    for product in low_stock:
        print(
            f"{product.get('name', 'Без названия')} - "
            f"остаток: {product.get('quantity', 0)}"
        )


def search_advanced(products, query, category=None, min_price=None, max_price=None):
    """Комбинированный поиск по названию/бренду, категории и диапазону цен."""
    result = []
    query = query.lower().strip() if query else ""

    for product in products:
        name = str(product.get("name", "")).lower()
        brand = str(product.get("brand", "")).lower()
        price = product.get("price", 0)

        if query and query not in name and query not in brand:
            continue
        if category and product.get("category", "") != category:
            continue
        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue
        result.append(product)

    return result


def find_by_name(products, name):
    """Находит товар по точному названию (без учёта регистра). Возвращает dict или None."""
    wanted = str(name).strip().lower()
    for product in products:
        if str(product.get("name", "")).strip().lower() == wanted:
            return product
    return None


def sort_products(products, key="name", reverse=False):
    """Возвращает новый список, отсортированный по полю key.

    Raises:
        ValueError: если key не входит в SORT_KEYS.
    """
    if key not in SORT_KEYS:
        raise ValueError(f"Нельзя сортировать по '{key}'. Допустимо: {', '.join(SORT_KEYS)}")
    return sorted(products, key=lambda product: product.get(key, ""), reverse=reverse)


def format_product(product):
    """Возвращает строку для вывода товара в каталоге."""
    return (
        f"{product.get('name', 'Без названия')} | {product.get('brand', '-')} | "
        f"{product.get('category', '-')} | {product.get('price', 0)} руб. | "
        f"в наличии: {product.get('quantity', 0)}"
    )
