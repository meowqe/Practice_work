# ===== Задание 1. Первая программа =====
print("Приложение Чудо Обувь запущено")
print("Добро пожаловать!")

# ===== Задание 2. Переменные, print, for =====
login = "admin"
last_name = "Админов"
price = 8990.0
quantity = 5
in_stock = True

print("Логин:", login)
print("Фамилия:", last_name)
print("Цена:", price, "руб.")
print("Количество:", quantity)
print("В наличии:", in_stock)

sizes = [36.0, 37.0, 38.0, 39.0]
print("\nДоступные размеры:")
for s in sizes:
    print("-", s)

print("\nНомера по порядку:")
for i in range(len(sizes)):
    print(i + 1, "—", sizes[i])

if quantity <= 3:
    print("\nМало на складе")
else:
    print("\nДостаточно на складе")

# ===== Задание 3. Списки и словари =====
users = [
    {'login': 'admin',   'last_name': 'Админов',      'role': 'администратор'},
    {'login': 'manager', 'last_name': 'Менеджеров',   'role': 'менеджер'},
    {'login': 'user',    'last_name': 'Пользователев', 'role': 'авторизованный'},
]

print("\nПользователи системы:")
for u in users:
    print(f"Логин: {u['login']}, фамилия: {u['last_name']}, роль: {u['role']}")

products = [
    {'id': 1, 'name': 'Air Max',   'price': 8990.0, 'sizes': {36.0: 5, 37.0: 2}},
    {'id': 2, 'name': 'Superstar', 'price': 7490.0, 'sizes': {37.0: 4, 38.0: 3}},
    {'id': 3, 'name': 'Runfalcon', 'price': 5590.0, 'sizes': {39.0: 2}},
]

print("\nКаталог товаров:")
for p in products:
    total_qty = sum(p['sizes'].values())
    print(f"{p['name']} — {p['price']} руб., всего на складе: {total_qty} шт.")

# ===== Задание 4. Функции =====
def find_user(login):
    for u in users:
        if u['login'] == login:
            return u
    return None


result = find_user('admin')
if result:
    print(f"\nНайден пользователь: {result['last_name']}")
else:
    print("\nПользователь не найден")


def total_sum(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total


cart = [
    {'name': 'Air Max',   'price': 8990.0, 'quantity': 2},
    {'name': 'Superstar', 'price': 7490.0, 'quantity': 1},
]

print(f"Итоговая сумма заказа: {total_sum(cart)} руб.")

# ===== Задание 5. Сортировка и фильтрация =====
sorted_by_price = sorted(products, key=lambda p: p['price'])
print("\nТовары по возрастанию цены:")
for p in sorted_by_price:
    print(f"{p['name']} — {p['price']} руб.")

low_stock = [p for p in products if sum(p['sizes'].values()) <= 3]
print("\nТовары с низким остатком (≤ 3 шт.):")
for p in low_stock:
    print(p['name'])

# ===== Задание 6. Поиск по каталогу =====
def search_products(query):
    query = query.lower()
    return [p for p in products if query in p['name'].lower()]


found = search_products('max')
print("\nРезультаты поиска 'max':")
for p in found:
    print(p['name'])


def filter_by_price(products, min_price, max_price):
    return [p for p in products if min_price <= p['price'] <= max_price]


result = filter_by_price(products, 5000, 8000)
print("\nТовары от 5000 до 8000 руб.:")
for p in result:
    print(f"{p['name']} — {p['price']} руб.")

# ===== Задание 7. Мини-задача «Корзина» =====
def add_to_cart(cart, product, size, quantity):
    cart.append({
        'product': product['name'],
        'price': product['price'],
        'size': size,
        'quantity': quantity
    })


def remove_from_cart(cart, name):
    cart[:] = [item for item in cart if item['product'] != name]


def change_quantity(cart, name, new_qty):
    for item in cart:
        if item['product'] == name:
            item['quantity'] = new_qty
            break


cart = []
add_to_cart(cart, products[0], 36.0, 2)
add_to_cart(cart, products[1], 37.0, 1)

print("\nКорзина:")
for item in cart:
    print(f"{item['product']}, размер {item['size']}, "
          f"{item['quantity']} шт. × {item['price']} = "
          f"{item['quantity'] * item['price']} руб.")

print(f"\nИтого: {total_sum(cart)} руб.")

change_quantity(cart, 'Air Max', 3)
remove_from_cart(cart, 'Superstar')

print("\nПосле изменений:")
for item in cart:
    print(f"{item['product']}, размер {item['size']}, {item['quantity']} шт.")
print(f"Итого: {total_sum(cart)} руб.")

# ===== Задание 8. Самостоятельно =====
print("\n===== Задание 8 =====")

# 1. Добавляем два новых товара
products.append({'id': 4, 'name': 'Gazelle',   'price': 9990.0, 'sizes': {40.0: 3, 41.0: 6, 42.0: 1}})
products.append({'id': 5, 'name': 'Duramo SL', 'price': 4590.0, 'sizes': {38.0: 7, 39.0: 4}})

# 2. Функция get_sizes
def get_sizes(product):
    return list(product['sizes'].keys())


# 3. Функция get_total_quantity
def get_total_quantity(product):
    return sum(product['sizes'].values())


print("\nРазмеры и количество по товарам:")
for p in products:
    print(f"{p['name']}: размеры {get_sizes(p)}, всего {get_total_quantity(p)} шт.")

# 4. Сортировка по названию
by_name = sorted(products, key=lambda p: p['name'])
print("\nТовары по алфавиту:")
for p in by_name:
    print(p['name'])

# 5. Товары дешевле 6000 рублей
cheap = [p for p in products if p['price'] < 6000]
print("\nТовары дешевле 6000 руб.:")
for p in cheap:
    print(f"{p['name']} — {p['price']} руб.")

# 6. Вывод товаров через while
print("\nВывод через while:")
i = 0
while i < len(products):
    p = products[i]
    print(f"{i + 1}. {p['name']} — {p['price']} руб.")
    i += 1

# ===== Дополнительное задание: заказы =====
orders = [
    {'date': '2025-03-15', 'client': 'Иванов',
     'items': [{'name': 'Air Max', 'price': 8990.0, 'quantity': 1},
               {'name': 'Superstar', 'price': 7490.0, 'quantity': 2}]},
    {'date': '2025-01-10', 'client': 'Петров',
     'items': [{'name': 'Runfalcon', 'price': 5590.0, 'quantity': 3}]},
    {'date': '2025-02-20', 'client': 'Сидорова',
     'items': [{'name': 'Gazelle', 'price': 9990.0, 'quantity': 1}]},
]

print("\nЗаказы по дате:")
for o in sorted(orders, key=lambda o: o['date']):
    print(f"{o['date']} — {o['client']}: {total_sum(o['items'])} руб.")
