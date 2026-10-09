import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orders import apply_discount, create_order, next_order_id, reduce_stock

CART = [{"name": "Мяч", "price": 100, "quantity": 2}]


class TestOrders(unittest.TestCase):
    def test_discount(self):
        self.assertEqual(apply_discount(1000, 10), 900)
        self.assertEqual(apply_discount(1000, 0), 1000)
        with self.assertRaises(ValueError):
            apply_discount(1000, 101)

    def test_create_order(self):
        order = create_order(CART, " Иван ", discount=10, order_id=7, created_at="2026-01-01 10:00:00")
        self.assertEqual(order["id"], 7)
        self.assertEqual(order["customer"], "Иван")
        self.assertEqual(order["total"], 180)
        self.assertIsNot(order["items"][0], CART[0])

    def test_create_order_errors(self):
        with self.assertRaises(ValueError):
            create_order([], "Иван")
        with self.assertRaises(ValueError):
            create_order(CART, "  ")

    def test_reduce_stock(self):
        products = [{"name": "Мяч", "quantity": 5}]
        reduce_stock(products, CART)
        self.assertEqual(products[0]["quantity"], 3)

    def test_reduce_stock_is_atomic(self):
        products = [{"name": "Мяч", "quantity": 5}, {"name": "Бутсы", "quantity": 0}]
        cart = CART + [{"name": "Бутсы", "price": 1, "quantity": 1}]
        with self.assertRaises(ValueError):
            reduce_stock(products, cart)
        self.assertEqual(products[0]["quantity"], 5)

    def test_next_order_id(self):
        self.assertEqual(next_order_id([]), 1)
        self.assertEqual(next_order_id([{"id": 3}, {"id": 1}]), 4)


if __name__ == "__main__":
    unittest.main()
