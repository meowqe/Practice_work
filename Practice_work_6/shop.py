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


def search_advanced(
    products,
    query,
    category=None,
    min_price=None,
    max_price=None
):
    """
    Комбинированный поиск товаров по названию/бренду,
    категории и диапазону цен.
    """
    result = []

    query = query.lower().strip() if query else ""

    for product in products:
        name = str(product.get("name", "")).lower()
        brand = str(product.get("brand", "")).lower()
        product_category = product.get("category", "")
        price = product.get("price", 0)

        # Поиск по названию или бренду
        if query and query not in name and query not in brand:
            continue

        # Фильтр по категории
        if category and product_category != category:
            continue

        # Минимальная цена
        if min_price is not None and price < min_price:
            continue

        # Максимальная цена
        if max_price is not None and price > max_price:
            continue

        result.append(product)

    return result


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


# Пример данных для проверки
if __name__ == "__main__":

    products = [
        {
            "name": "Футбольный мяч",
            "brand": "Adidas",
            "category": "Мячи",
            "price": 2500,
            "quantity": 2
        },
        {
            "name": "Баскетбольный мяч",
            "brand": "Nike",
            "category": "Мячи",
            "price": 3000,
            "quantity": 5
        },
        {
            "name": "Футбольные бутсы",
            "brand": "Puma",
            "category": "Обувь",
            "price": 6500,
            "quantity": 3
        },
        {
            "name": "Спортивная форма",
            "brand": "Adidas",
            "category": "Одежда",
            "price": 4500,
            "quantity": 10
        }
    ]

    # 1. Товары с низким остатком
    print("=== Низкий остаток ===")
    highlight_low_stock(products)

    # 2. Комбинированный поиск
    print("\n=== Поиск ===")
    results = search_advanced(
        products,
        query="adidas",
        min_price=2000,
        max_price=5000
    )

    for product in results:
        print(product)

    # 3. Количество товаров по категориям
    print("\n=== Категории ===")
    print(count_by_category(products))

    # 4. Сохранение заказов
    print("\n=== Сохранение заказа ===")

    orders = [
        {
            "product": "Футбольный мяч",
            "quantity": 2
        },
        {
            "product": "Спортивная форма",
            "quantity": 1
        }
    ]

    save_orders(orders)
