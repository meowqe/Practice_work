import os
import unittest
from src.orders import create_order, save_orders, load_orders

P = [{"id": 1, "name": "Кроссовки", "category": "Обувь", "price": 100.0, "sizes": {"40": 10}}]
CART = [{"product_id": 1, "name": "Кроссовки", "size": 40, "quantity": 2, "price": 100.0}]


class TestOrders(unittest.TestCase):
    def test_create(self):
        o = create_order(CART, "Анна", P)
        self.assertEqual(o["total"], 200.0)
        self.assertEqual(o["client"], "Анна")

    def test_empty_cart_or_name(self):
        self.assertIsNone(create_order([], "Анна", P))
        self.assertIsNone(create_order(CART, "  ", P))

    def test_save_load(self):
        f = "data/_test_orders_unit.json"
        try:
            save_orders([create_order(CART, "Анна", P)], f)
            self.assertEqual(len(load_orders(f)), 1)
        finally:
            if os.path.exists(f):
                os.remove(f)
        self.assertEqual(load_orders(f), [])


if __name__ == "__main__":
    unittest.main()
