import os
import unittest

from src.catalog import get_low_stock
from src.cart import add_to_cart, cart_total
from src.orders import create_order, save_orders, load_orders
from src.analytics import total_revenue, best_selling_product
from src.storage import load_products


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.products = load_products('data/products.json')
        self.cart = []
        self.orders_file = 'data/test_orders.json'

    def tearDown(self):
        if os.path.exists(self.orders_file):
            os.remove(self.orders_file)

    def test_full_cycle(self):
        # Добавляем товар в корзину
        result, msg = add_to_cart(self.cart, self.products, 1, 40, 2)
        self.assertTrue(result)

        # Создаём заказ
        order = create_order(self.cart, 'Тестовый клиент', self.products)
        self.assertIsNotNone(order)
        self.assertGreater(order['total'], 0)
        self.assertEqual(order['total'], cart_total(self.cart))

        # Сохраняем и загружаем
        save_orders([order], self.orders_file)
        loaded = load_orders(self.orders_file)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]['total'], order['total'])

    def test_cart_to_analytics(self):
        add_to_cart(self.cart, self.products, 1, 40, 2)
        add_to_cart(self.cart, self.products, 3, "M", 1)
        order = create_order(self.cart, 'Клиент', self.products)
        save_orders([order], self.orders_file)
        loaded = load_orders(self.orders_file)
        self.assertEqual(total_revenue(loaded), 8990.0 * 2 + 1990.0)
        self.assertEqual(best_selling_product(loaded)[1], 2)

    def test_low_stock_warning_reaches_cart(self):
        low_ids = [p['id'] for p in get_low_stock(self.products)]
        self.assertIn(2, low_ids)
        ok, msg = add_to_cart(self.cart, self.products, 2, 40, 1)
        self.assertTrue(ok)
        self.assertIn('мал', msg)


if __name__ == '__main__':
    unittest.main()
