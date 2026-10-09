import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import contextlib
import io
import json
import shutil
import tempfile

import main as app

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        shutil.copy(os.path.join(ROOT, "data", "products.json"), self.tmp.name)

    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = app.main(["--data-dir", self.tmp.name, *argv])
        return code, out.getvalue(), err.getvalue()

    def test_catalog_and_search(self):
        code, out, _ = self.run_cli("catalog")
        self.assertEqual(code, 0)
        self.assertEqual(len(out.strip().splitlines()), 8)
        _, out, _ = self.run_cli("search", "adidas", "--min-price", "2000", "--max-price", "5000")
        self.assertEqual(len(out.strip().splitlines()), 2)

    def test_full_purchase_scenario(self):
        self.assertEqual(self.run_cli("cart", "add", "Скакалка", "-q", "2")[0], 0)
        _, out, _ = self.run_cli("cart", "show")
        self.assertIn("Итого: 1400", out)
        code, out, _ = self.run_cli("checkout", "--customer", "Иван", "--discount", "10")
        self.assertEqual(code, 0)
        self.assertIn("Сумма: 1260 руб.", out)
        _, out, _ = self.run_cli("orders")
        self.assertIn("Иван", out)
        with open(os.path.join(self.tmp.name, "products.json"), encoding="utf-8") as f:
            stock = {p["name"]: p["quantity"] for p in json.load(f)}
        self.assertEqual(stock["Скакалка"], 13)
        _, out, _ = self.run_cli("analytics")
        self.assertIn("выручка: 1260", out)

    def test_errors_return_code_1(self):
        code, _, err = self.run_cli("cart", "add", "Лыжи")
        self.assertEqual(code, 1)
        self.assertIn("не найден", err)
        code, _, err = self.run_cli("checkout", "--customer", "Иван")
        self.assertEqual(code, 1)
        self.assertIn("пуста", err)
        code, _, _ = self.run_cli("cart", "add", "Гантели 5 кг", "-q", "5")
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
