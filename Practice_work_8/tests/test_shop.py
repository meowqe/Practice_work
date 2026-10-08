import contextlib
import io
import json
import os
import tempfile
import unittest

from shop import (get_low_stock, highlight_low_stock, search_advanced,
                  count_by_category, save_orders, total_sum, cart_total,
                  add_to_cart, remove_from_cart, update_quantity)


def make_products():
    return [
        {'id': 1, 'name': 'Футбольный мяч', 'brand': 'Adidas', 'category': 'Мячи',
         'price': 2500, 'quantity': 2, 'sizes': {5: 2}},
        {'id': 2, 'name': 'Баскетбольный мяч', 'brand': 'Nike', 'category': 'Мячи',
         'price': 3000, 'quantity': 5, 'sizes': {7: 5}},
        {'id': 3, 'name': 'Футбольные бутсы', 'brand': 'Puma', 'category': 'Обувь',
         'price': 6500, 'quantity': 3, 'sizes': {40: 2, 41: 1}},
        {'id': 4, 'name': 'Спортивная форма', 'brand': 'Adidas', 'category': 'Одежда',
         'price': 4500, 'quantity': 10, 'sizes': {46: 10}},
    ]


class TestGetLowStock(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(get_low_stock([]), [])

    def test_no_low_stock(self):
        products = [{'name': 'A', 'sizes': {40: 10}}]
        self.assertEqual(get_low_stock(products), [])

    def test_one_low_stock(self):
        products = [
            {'name': 'A', 'sizes': {40: 1}},
            {'name': 'B', 'sizes': {40: 10}},
        ]
        result = get_low_stock(products)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'A')

    def test_sizes_are_summed(self):
        products = [{'name': 'A', 'sizes': {40: 1, 41: 1}},
                    {'name': 'B', 'sizes': {40: 10, 41: 10}}]
        self.assertEqual([p['name'] for p in get_low_stock(products)], ['A'])

    def test_quantity_field(self):
        result = get_low_stock(make_products())
        self.assertEqual([p['id'] for p in result], [1, 3])

    def test_boundary_three_is_low_four_is_not(self):
        self.assertEqual(len(get_low_stock([{'name': 'A', 'quantity': 3}])), 1)
        self.assertEqual(get_low_stock([{'name': 'A', 'quantity': 4}]), [])

    def test_sorted_by_quantity(self):
        products = [{'name': 'A', 'quantity': 3}, {'name': 'B', 'quantity': 1}]
        self.assertEqual([p['name'] for p in get_low_stock(products)], ['B', 'A'])


class TestHighlightLowStock(unittest.TestCase):
    def _run(self, products):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            highlight_low_stock(products)
        return buf.getvalue()

    def test_prints_low_stock(self):
        out = self._run(make_products())
        self.assertIn('Футбольный мяч', out)
        self.assertNotIn('Спортивная форма', out)

    def test_prints_message_when_none(self):
        self.assertIn('Нет товаров', self._run([]))


class TestSearchAdvanced(unittest.TestCase):
    def setUp(self):
        self.products = make_products()

    def test_search_by_name(self):
        result = search_advanced(self.products, 'бутсы')
        self.assertEqual([p['id'] for p in result], [3])

    def test_search_by_brand(self):
        result = search_advanced(self.products, 'ADIDAS')
        self.assertEqual([p['id'] for p in result], [1, 4])

    def test_search_by_category(self):
        result = search_advanced(self.products, '', category='Мячи')
        self.assertEqual([p['id'] for p in result], [1, 2])

    def test_search_by_price(self):
        result = search_advanced(self.products, '', min_price=3000, max_price=5000)
        self.assertEqual([p['id'] for p in result], [2, 4])

    def test_combined(self):
        result = search_advanced(self.products, 'adidas', min_price=2000, max_price=5000)
        self.assertEqual([p['id'] for p in result], [1, 4])

    def test_empty_query_returns_all(self):
        self.assertEqual(len(search_advanced(self.products, '')), 4)
        self.assertEqual(len(search_advanced(self.products, None)), 4)

    def test_nothing_found(self):
        self.assertEqual(search_advanced(self.products, 'reebok'), [])


class TestCountByCategory(unittest.TestCase):
    def test_count(self):
        self.assertEqual(count_by_category(make_products()),
                         {'Мячи': 2, 'Обувь': 1, 'Одежда': 1})

    def test_empty(self):
        self.assertEqual(count_by_category([]), {})

    def test_no_category(self):
        self.assertEqual(count_by_category([{'name': 'X'}]), {'Без категории': 1})


class TestSaveOrders(unittest.TestCase):
    def test_save_and_load(self):
        orders = [{'product': 'Футбольный мяч', 'quantity': 2}]
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, 'orders.json')
            with contextlib.redirect_stdout(io.StringIO()):
                save_orders(orders, path)
            with open(path, encoding='utf-8') as f:
                self.assertEqual(json.load(f), orders)


class TestTotalSum(unittest.TestCase):
    def test_empty_cart(self):
        self.assertEqual(total_sum([]), 0)

    def test_cart_with_items(self):
        items = [{'price': 100, 'qty': 2}, {'price': 50, 'qty': 1}]
        self.assertEqual(total_sum(items), 250)


class TestAddToCart(unittest.TestCase):
    def setUp(self):
        self.products = make_products()
        self.cart = []

    def test_invalid_size(self):
        products = [{'id': 1, 'name': 'A', 'sizes': {40: 5}}]
        cart = []
        result, message = add_to_cart(cart, products, 1, 99, 1)
        self.assertFalse(result)
        self.assertIn('размер', message.lower())
        self.assertEqual(cart, [])

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            _ = 1 / 0

    def test_add_success(self):
        ok, _ = add_to_cart(self.cart, self.products, 3, 40, 2)
        self.assertTrue(ok)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart[0]['qty'], 2)

    def test_add_twice_increases_quantity(self):
        add_to_cart(self.cart, self.products, 3, 40, 1)
        ok, _ = add_to_cart(self.cart, self.products, 3, 40, 1)
        self.assertTrue(ok)
        self.assertEqual(len(self.cart), 1)
        self.assertEqual(self.cart[0]['qty'], 2)

    def test_add_more_than_stock(self):
        ok, message = add_to_cart(self.cart, self.products, 3, 41, 5)
        self.assertFalse(ok)
        self.assertIn('недостаточно', message.lower())

    def test_add_twice_over_stock(self):
        add_to_cart(self.cart, self.products, 3, 41, 1)
        ok, _ = add_to_cart(self.cart, self.products, 3, 41, 1)
        self.assertFalse(ok)
        self.assertEqual(self.cart[0]['qty'], 1)

    def test_add_unknown_product(self):
        ok, _ = add_to_cart(self.cart, self.products, 999, 40, 1)
        self.assertFalse(ok)


class TestCartOperations(unittest.TestCase):
    def setUp(self):
        self.products = make_products()
        self.cart = []
        add_to_cart(self.cart, self.products, 2, 7, 2)   # 3000 * 2
        add_to_cart(self.cart, self.products, 4, 46, 1)  # 4500 * 1

    def test_remove_from_cart(self):
        self.assertTrue(remove_from_cart(self.cart, 2, 7))
        self.assertEqual([i['id'] for i in self.cart], [4])

    def test_remove_missing_item(self):
        self.assertFalse(remove_from_cart(self.cart, 3, 40))
        self.assertEqual(len(self.cart), 2)

    def test_update_quantity(self):
        self.assertTrue(update_quantity(self.cart, 2, 7, 4))
        self.assertEqual(self.cart[0]['qty'], 4)

    def test_update_quantity_zero_removes(self):
        update_quantity(self.cart, 4, 46, 0)
        self.assertEqual(len(self.cart), 1)

    def test_update_missing_item(self):
        self.assertFalse(update_quantity(self.cart, 3, 40, 1))

    def test_cart_total(self):
        self.assertEqual(cart_total(self.cart), 10500)

    def test_cart_total_with_discount(self):
        self.assertEqual(cart_total(self.cart, discount=10), 9450.0)

    def test_cart_total_empty(self):
        self.assertEqual(cart_total([]), 0)


if __name__ == '__main__':
    unittest.main()
