"""Точка входа приложения «СпортТовары» (демонстрационный сценарий)."""
from src.catalog import get_low_stock, search_advanced, count_by_category, avg_price
from src.cart import add_to_cart, cart_total
from src.orders import create_order, print_order, save_orders, load_orders
from src.analytics import total_revenue, best_selling_product, average_order_total
from src.storage import load_products

PRODUCTS_FILE = "data/products.json"
ORDERS_FILE = "data/orders.json"


def main():
    products = load_products(PRODUCTS_FILE)
    print(f"Загружено товаров: {len(products)}")
    print("Товаров по категориям:", count_by_category(products))
    print("Средняя цена:", avg_price(products))
    print("Мало на складе:", [p["name"] for p in get_low_stock(products)])
    print("Поиск 'кроссовки' до 10000:",
          [p["name"] for p in search_advanced(products, "кроссовки", max_price=10000)])

    cart = []
    for pid, size, qty in [(1, 40, 2), (3, "M", 1), (5, 5, 1)]:
        ok, msg = add_to_cart(cart, products, pid, size, qty)
        print(f"add_to_cart({pid}, {size}, {qty}): {msg}")
    print("Сумма корзины:", cart_total(cart))

    order = create_order(cart, "Иван Петров", products)
    print_order(order)

    orders = load_orders(ORDERS_FILE)
    orders.append(order)
    save_orders(orders, ORDERS_FILE)
    print("Выручка:", total_revenue(orders))
    print("Хит продаж:", best_selling_product(orders))
    print("Средний чек:", average_order_total(orders))


if __name__ == "__main__":
    main()
