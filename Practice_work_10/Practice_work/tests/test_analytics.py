import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analytics import (average_price, count_by_category, stock_value,
                           top_products, total_revenue)

PRODUCTS = [
    {"category": "Мячи", "price": 100, "quantity": 2},
    {"category": "Мячи", "price": 300, "quantity": 1},
    {"category": "Обувь", "price": 500, "quantity": 4},
]
ORDERS = [
    {"total": 250.5, "items": [{"name": "Мяч", "quantity": 2}]},
    {"total": 100, "items": [{"name": "Мяч", "quantity": 1}, {"name": "Бутсы", "quantity": 5}]},
]


class TestAnalytics(unittest.TestCase):
    def test_count_by_category(self):
        self.assertEqual(count_by_category(PRODUCTS), {"Мячи": 2, "Обувь": 1})

    def test_average_and_stock(self):
        self.assertEqual(average_price(PRODUCTS), 300)
        self.assertEqual(average_price([]), 0.0)
        self.assertEqual(stock_value(PRODUCTS), 2500)

    def test_revenue_and_top(self):
        self.assertEqual(total_revenue(ORDERS), 350.5)
        self.assertEqual(top_products(ORDERS, 1), [("Бутсы", 5)])
        self.assertEqual(top_products([]), [])


if __name__ == "__main__":
    unittest.main()
