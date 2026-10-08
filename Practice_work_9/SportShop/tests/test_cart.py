import unittest
from src.cart import add_to_cart, remove_from_cart, update_quantity, cart_total

P = [{"id": 1, "name": "Кроссовки", "category": "Обувь", "price": 100.0, "sizes": {"40": 10, "41": 1}}]


class TestCart(unittest.TestCase):
    def setUp(self):
        self.cart = []

    def test_add_and_total(self):
        ok, _ = add_to_cart(self.cart, P, 1, 40, 2)
        self.assertTrue(ok)
        self.assertEqual(cart_total(self.cart), 200.0)

    def test_add_errors(self):
        self.assertFalse(add_to_cart(self.cart, P, 99, 40, 1)[0])
        self.assertFalse(add_to_cart(self.cart, P, 1, 50, 1)[0])
        self.assertFalse(add_to_cart(self.cart, P, 1, 41, 5)[0])
        self.assertFalse(add_to_cart(self.cart, P, 1, 40, 0)[0])

    def test_update_remove(self):
        add_to_cart(self.cart, P, 1, 40, 1)
        self.assertTrue(update_quantity(self.cart, P, 1, 40, 3)[0])
        self.assertEqual(cart_total(self.cart), 300.0)
        self.assertFalse(update_quantity(self.cart, P, 1, 40, 99)[0])
        self.assertTrue(remove_from_cart(self.cart, 1, 40)[0])
        self.assertEqual(self.cart, [])


if __name__ == "__main__":
    unittest.main()
