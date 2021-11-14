import pytest


class Product:
    def __init__(self, name: str, unit: str, price: int) -> None:
        if unit not in ('kg', 'item'):
            raise Exception

        if name is None:
            raise Exception

        if price < 0:
            raise Exception

        self.unit = unit
        self.name = name
        self.price = price


def test_create_product():
    product = Product(name='Banana', unit='kg', price=499)

    assert product.name == 'Banana'
    assert product.unit == 'kg'
    assert product.price == 499


def test_create_product_with_incorrect_unit():
    with pytest.raises(Exception):
        Product(name='Banana', unit='test', price=499)


def test_create_product_without_unit():
    with pytest.raises(Exception):
        Product(name='Banana', price=499)


def test_create_product_with_incorrect_price():
    with pytest.raises(Exception):
        Product(name='Banana', price=0)

    with pytest.raises(Exception):
        Product(name='Banana', price=-1)


class Warehouse:
    __products = []

    def add(self, product: Product):
        self.__products.append(product)

    def products(self):
        return self.__products

    def get(self, name):
        for product in self.__products:
            if product.name == name:
                return product

        raise Exception()


def test_add_product_to_warehouse():
    warehouse = Warehouse()
    warehouse.add(Product(name='Banana', unit='kg', price=499))

    assert 1 == len(warehouse.products())


def test_get_product_from_warehouse_by_name():
    warehouse = Warehouse()
    warehouse.add(Product(name='Banana', unit='kg', price=499))

    assert 'Banana' == warehouse.get(name='Banana').name


def test_raise_exception_when_product_not_found_in_warehouse():
    with pytest.raises(Exception):
        Warehouse().get('Avocado')


class CashRegister:
    def __init__(self, warehouse: Warehouse) -> None:
        self.warehouse = warehouse
        self.orders = []

    def order(self, name: str, quantity: int):
        self.orders.append((name, quantity))

    def bill(self):
        sum = 0
        for order in self.orders:
            product = self.warehouse.get(order[0])

            sum += product.price * order[1]

        return Bill(sum=sum)


def test_order_two_kg_of_product_in_cash_register():
    warehouse = Warehouse()
    warehouse.add(Product(name='Banana', unit='kg', price=499))

    cash_register = CashRegister(warehouse)

    cash_register.order(name='Banana', quantity=2)

    assert 998 == cash_register.bill().sum


class Bill:
    def __init__(self, sum: int) -> None:
        self.sum = sum


def test_order_on_cash_register_and_return_bill():
    warehouse = Warehouse()
    warehouse.add(Product(name='Banana', unit='kg', price=499))

    cash_register = CashRegister(warehouse)

    cash_register.order(name='Banana', quantity=2)

    assert Bill == type(cash_register.bill())


