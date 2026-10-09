import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.catalog import (find_by_name, format_product, get_low_stock,
                         search_advanced, sort_products)

PRODUCTS = [
    {"name": "Мяч", "brand": "Adidas", "category": "Мячи", "price": 2500, "quantity": 2},
    {"name": "Бутсы", "brand": "Puma", "category": "Обувь", "price": 6500, "quantity": 3},
    {"name": "Форма", "brand": "Adidas", "category": "Одежда", "price": 4500, "quantity": 10},
]


class TestCatalog(unittest.TestCase):
    def test_low_stock_sorted(self):
        names = [p["name"] for p in get_low_stock(PRODUCTS)]
        self.assertEqual(names, ["Мяч", "Бутсы"])

    def test_low_stock_threshold(self):
        self.assertEqual(len(get_low_stock(PRODUCTS, threshold=10)), 3)

    def test_search_filters(self):
        self.assertEqual(len(search_advanced(PRODUCTS, "adidas", max_price=3000)), 1)
        self.assertEqual(len(search_advanced(PRODUCTS, "", category="Обувь")), 1)

    def test_find_by_name_case_insensitive(self):
        self.assertEqual(find_by_name(PRODUCTS, " мяч ")["brand"], "Adidas")
        self.assertIsNone(find_by_name(PRODUCTS, "Лыжи"))

    def test_sort_products(self):
        prices = [p["price"] for p in sort_products(PRODUCTS, "price", reverse=True)]
        self.assertEqual(prices, [6500, 4500, 2500])
        with self.assertRaises(ValueError):
            sort_products(PRODUCTS, "color")

    def test_format_product(self):
        self.assertIn("2500 руб.", format_product(PRODUCTS[0]))


if __name__ == "__main__":
    unittest.main()
