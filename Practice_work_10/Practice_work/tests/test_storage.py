import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tempfile

from src import storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def path(self, name):
        return os.path.join(self.tmp.name, name)

    def test_roundtrip_unicode_and_new_folder(self):
        orders = [{"customer": "Иван", "total": 100}]
        file = self.path("sub/orders.json")
        storage.save_orders(orders, file)
        self.assertEqual(storage.load_orders(file), orders)

    def test_missing_orders_is_empty(self):
        self.assertEqual(storage.load_orders(self.path("none.json")), [])

    def test_missing_products_raises(self):
        with self.assertRaises(FileNotFoundError):
            storage.load_products(self.path("none.json"))

    def test_bad_json_raises(self):
        file = self.path("bad.json")
        with open(file, "w", encoding="utf-8") as f:
            f.write("{oops")
        with self.assertRaises(ValueError):
            storage.load_json(file)


if __name__ == "__main__":
    unittest.main()
