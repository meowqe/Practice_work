import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shop import search_advanced

PRODUCTS = [
    {"name": "Футбольный мяч", "brand": "Adidas", "category": "Мячи", "price": 2500, "quantity": 2},
    {"name": "Баскетбольный мяч", "brand": "Nike", "category": "Мячи", "price": 3000, "quantity": 5},
    {"name": "Футбольные бутсы", "brand": "Puma", "category": "Обувь", "price": 6500, "quantity": 3},
    {"name": "Спортивная форма", "brand": "Adidas", "category": "Одежда", "price": 4500, "quantity": 10},
]


class TestSearchAdvanced(unittest.TestCase):
    def test_by_brand_and_price(self):
        res = search_advanced(PRODUCTS, "adidas", min_price=2000, max_price=5000)
        self.assertEqual(len(res), 2)

    def test_by_category(self):
        res = search_advanced(PRODUCTS, "", category="Обувь")
        self.assertEqual([p["brand"] for p in res], ["Puma"])

    def test_no_match(self):
        self.assertEqual(search_advanced(PRODUCTS, "xyz"), [])


if __name__ == "__main__":
    unittest.main()
