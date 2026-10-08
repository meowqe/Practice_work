import unittest
from src.catalog import get_low_stock, search_advanced, count_by_category, avg_price

P = [
    {"id": 1, "name": "Кроссовки A", "category": "Обувь", "price": 100.0, "sizes": {"40": 2}},
    {"id": 2, "name": "Футболка B", "category": "Одежда", "price": 300.0, "sizes": {"M": 20}},
]


class TestCatalog(unittest.TestCase):
    def test_low_stock(self):
        self.assertEqual([p["id"] for p in get_low_stock(P)], [1])

    def test_search(self):
        self.assertEqual(len(search_advanced(P, "кросс")), 1)
        self.assertEqual(len(search_advanced(P, "", category="одежда")), 1)
        self.assertEqual(len(search_advanced(P, "", min_price=200)), 1)
        self.assertEqual(len(search_advanced(P, "", max_price=50)), 0)

    def test_count_and_avg(self):
        self.assertEqual(count_by_category(P), {"Обувь": 1, "Одежда": 1})
        self.assertEqual(avg_price(P), 200.0)
        self.assertEqual(avg_price([]), 0.0)


if __name__ == "__main__":
    unittest.main()
