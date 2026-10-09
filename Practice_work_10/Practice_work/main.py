"""СпортТовары — система управления магазином (консольное приложение)."""
import argparse
import os
import sys

from src import analytics, cart as cart_lib, catalog, orders as orders_lib, storage

VERSION = "1.0"
ROOT = os.path.dirname(os.path.abspath(__file__))


def build_parser():
    parser = argparse.ArgumentParser(prog="main.py", description="СпортТовары — управление магазином")
    parser.add_argument("--data-dir", default=os.environ.get("SPORTSHOP_DATA", os.path.join(ROOT, "data")),
                        help="папка с данными (по умолчанию data/)")
    parser.add_argument("--version", action="version", version=f"СпортТовары {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("catalog", help="показать каталог")
    p.add_argument("--sort", choices=catalog.SORT_KEYS, default="name")
    p.add_argument("--desc", action="store_true", help="по убыванию")

    p = sub.add_parser("search", help="поиск товаров")
    p.add_argument("query", nargs="?", default="")
    p.add_argument("--category")
    p.add_argument("--min-price", type=float)
    p.add_argument("--max-price", type=float)

    sub.add_parser("low-stock", help="товары с низким остатком (<= 3)")

    p = sub.add_parser("cart", help="корзина")
    csub = p.add_subparsers(dest="action", required=True)
    a = csub.add_parser("add", help="добавить товар")
    a.add_argument("name")
    a.add_argument("-q", "--quantity", type=int, default=1)
    csub.add_parser("show", help="показать корзину")
    r = csub.add_parser("remove", help="удалить позицию")
    r.add_argument("name")
    csub.add_parser("clear", help="очистить корзину")

    p = sub.add_parser("checkout", help="оформить заказ")
    p.add_argument("--customer", required=True)
    p.add_argument("--discount", type=float, default=0)

    p = sub.add_parser("orders", help="показать сохранённые заказы")
    p.add_argument("--export", metavar="FILE", help="сохранить копию заказов в файл")

    sub.add_parser("analytics", help="аналитика")
    return parser


def _paths(data_dir):
    return (os.path.join(data_dir, "products.json"),
            os.path.join(data_dir, "cart.json"),
            os.path.join(data_dir, "orders.json"))


def _print_cart(cart):
    if not cart:
        print("Корзина пуста")
        return
    for i in cart:
        print(f"{i['name']} x{i['quantity']} = {i['price'] * i['quantity']} руб.")
    print(f"Итого: {cart_lib.cart_total(cart)} руб.")


def run(args):
    products_file, cart_file, orders_file = _paths(args.data_dir)
    products = storage.load_products(products_file)
    cmd = args.command

    if cmd == "catalog":
        for product in catalog.sort_products(products, args.sort, args.desc):
            print(catalog.format_product(product))

    elif cmd == "search":
        found = catalog.search_advanced(products, args.query, args.category, args.min_price, args.max_price)
        if not found:
            print("Ничего не найдено")
        for product in found:
            print(catalog.format_product(product))

    elif cmd == "low-stock":
        catalog.highlight_low_stock(products)

    elif cmd == "cart":
        cart = storage.load_json(cart_file, default=[])
        if args.action == "add":
            product = catalog.find_by_name(products, args.name)
            if product is None:
                raise KeyError(f"Товар '{args.name}' не найден")
            cart_lib.add_to_cart(cart, product, args.quantity)
            print(f"Добавлено: {product['name']} x{args.quantity}")
        elif args.action == "remove":
            cart_lib.remove_from_cart(cart, args.name)
            print(f"Удалено: {args.name}")
        elif args.action == "clear":
            cart_lib.clear_cart(cart)
            print("Корзина очищена")
        else:
            _print_cart(cart)
        if args.action != "show":
            storage.save_json(cart, cart_file)

    elif cmd == "checkout":
        cart = storage.load_json(cart_file, default=[])
        saved = storage.load_orders(orders_file)
        order = orders_lib.create_order(cart, args.customer, args.discount,
                                        order_id=orders_lib.next_order_id(saved))
        orders_lib.reduce_stock(products, cart)
        saved.append(order)
        storage.save_orders(saved, orders_file)
        storage.save_products(products, products_file)
        storage.save_json([], cart_file)
        print(f"Заказ №{order['id']} оформлен. Покупатель: {order['customer']}. "
              f"Сумма: {order['total']} руб.")

    elif cmd == "orders":
        saved = storage.load_orders(orders_file)
        if not saved:
            print("Заказов пока нет")
        for o in saved:
            items = ", ".join(f"{i['name']} x{i['quantity']}" for i in o["items"])
            print(f"№{o['id']} | {o['customer']} | {items} | {o['total']} руб.")
        if args.export:
            storage.save_orders(saved, args.export)
            print(f"Заказы сохранены в файл {args.export}")

    elif cmd == "analytics":
        saved = storage.load_orders(orders_file)
        print("Товаров по категориям:")
        for category, count in analytics.count_by_category(products).items():
            print(f"  {category}: {count}")
        print(f"Средняя цена: {analytics.average_price(products)} руб.")
        print(f"Стоимость остатков: {analytics.stock_value(products)} руб.")
        print(f"Заказов: {len(saved)}, выручка: {analytics.total_revenue(saved)} руб.")
        top = analytics.top_products(saved)
        if top:
            print("Топ товаров: " + ", ".join(f"{n} ({q} шт.)" for n, q in top))


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        run(args)
    except (ValueError, KeyError, FileNotFoundError) as error:
        message = error.args[0] if isinstance(error, KeyError) and error.args else error
        print(f"Ошибка: {message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
