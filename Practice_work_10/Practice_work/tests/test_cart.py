import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cart import (add_to_cart, cart_count, cart_total, clear_cart,
                      remove_from_cart, total_sum)

BALL = {"name": "Мяч", "price": 100, "quantity": 5}


class TestCart(unittest.TestCase):
    def test_add_and_merge(self):
        cart = []
        add_to_cart(cart, BALL, 2)
        add_to_cart(cart, BALL, 1)
        self.assertEqual(cart, [{"name": "Мяч", "price": 100, "quantity": 3}])

    def test_add_invalid(self):
        with self.assertRaises(ValueError):
            add_to_cart([], BALL, 0)
        with self.assertRaises(ValueError):
            add_to_cart([], BALL, 6)

    def test_total_regression_hotfix(self):
        # Регрессия hotfix/cart-total: количество обязано учитываться
        self.assertEqual(cart_total([{"price": 100, "quantity": 2}, {"price": 50}]), 250)

    def test_remove_and_clear(self):
        cart = [{"name": "Мяч", "price": 100, "quantity": 1}]
        remove_from_cart(cart, "мяч")
        self.assertEqual(cart, [])
        with self.assertRaises(KeyError):
            remove_from_cart(cart, "Мяч")
        add_to_cart(cart, BALL)
        self.assertEqual(clear_cart(cart), [])

    def test_count_and_total_sum(self):
        self.assertEqual(cart_count([{"quantity": 2}, {"quantity": 3}]), 5)
        self.assertEqual(total_sum([{"price": 100, "quantity": 2}]), 200)


if __name__ == "__main__":
    unittest.main()
