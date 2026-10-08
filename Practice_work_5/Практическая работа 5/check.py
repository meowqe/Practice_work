import io, contextlib, runpy, re

def run(src_patch=None):
    src = open('main.py', encoding='utf-8').read()
    if src_patch:
        src = src_patch(src)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ns = {}
        exec(compile(src, 'main.py', 'exec'), ns)
    return buf.getvalue(), ns

res = []
def check(name, cond):
    res.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), name)

out, ns = run()
check("T1 запуск без исключений", True)
check("T2 приветствие выводится", "Приложение Чудо Обувь запущено" in out and "Добро пожаловать!" in out)
check("T3 quantity=5 -> 'Достаточно на складе'", "Достаточно на складе" in out and "Мало на складе" not in out)
out2, _ = run(lambda s: s.replace("quantity = 5", "quantity = 2", 1))
check("T4 quantity=2 -> 'Мало на складе'", "Мало на складе" in out2)
check("T5 find_user('admin') найден", ns['find_user']('admin')['last_name'] == 'Админов')
check("T6 find_user('nobody') -> None", ns['find_user']('nobody') is None)
check("T7 total_sum(пустой список) == 0", ns['total_sum']([]) == 0)
check("T8 total_sum тестовой корзины == 25470.0", ns['total_sum']([{'price':8990.0,'quantity':2},{'price':7490.0,'quantity':1}]) == 25470.0)
check("T9 search 'max' -> Air Max", [p['name'] for p in ns['search_products']('max')] == ['Air Max'])
check("T10 search 'MAX' (регистр) -> Air Max", len(ns['search_products']('MAX')) == 1)
check("T11 search 'xyz' -> пусто", ns['search_products']('xyz') == [])
check("T12 filter_by_price границы включительно", [p['name'] for p in ns['filter_by_price'](ns['products'], 5590.0, 5590.0)] == ['Runfalcon'])
check("T13 filter_by_price 5000-8000 -> Superstar, Runfalcon", [p['name'] for p in ns['filter_by_price'](ns['products'],5000,8000)] == ['Superstar','Runfalcon'])
check("T14 корзина: итог после изменений 26970.0", "Итого: 26970.0 руб." in out)
check("T15 корзина: Superstar удалён", all(i['product']!='Superstar' for i in ns['cart']))
check("T16 get_sizes(Gazelle)", ns['get_sizes'](ns['products'][3]) == [40.0,41.0,42.0])
check("T17 get_total_quantity(Duramo SL) == 11", ns['get_total_quantity'](ns['products'][4]) == 11)
check("T18 сортировка по названию", [p['name'] for p in sorted(ns['products'], key=lambda p:p['name'])] == ['Air Max','Duramo SL','Gazelle','Runfalcon','Superstar'])
check("T19 дешевле 6000 -> Runfalcon, Duramo SL", [p['name'] for p in ns['cheap']] == ['Runfalcon','Duramo SL'])
check("T20 while выводит 5 товаров", len(re.findall(r'^\d\. ', out.split('Вывод через while:')[1], re.M)) == 5)
check("T21 заказы отсортированы по дате", out.split('Заказы по дате:')[1].split()[0] == '2025-01-10')
print(sum(r[1] for r in res), '/', len(res))
