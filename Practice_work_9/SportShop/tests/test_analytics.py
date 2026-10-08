import unittest
from src.analytics import total_revenue, best_selling_product, average_order_total

ORDERS = [
    {"total": 300.0, "items": [{"name": "A", "quantity": 2}, {"name": "B", "quantity": 1}]},
    {"total": 100.0, "items": [{"name": "B", "quantity": 3}]},
]


class TestAnalytics(unittest.TestCase):
    def test_all(self):
        self.assertEqual(total_revenue(ORDERS), 400.0)
        self.assertEqual(best_selling_product(ORDERS), ("B", 4))
        self.assertEqual(average_order_total(ORDERS), 200.0)

    def test_empty(self):
        self.assertEqual(total_revenue([]), 0)
        self.assertIsNone(best_selling_product([]))
        self.assertEqual(average_order_total([]), 0.0)


if __name__ == "__main__":
    unittest.main()
