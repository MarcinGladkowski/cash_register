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


class Warehouse:

    def __init__(self) -> None:
        self.__products = []

    def add(self, product: Product):
        self.__products.append(product)

    def products(self):
        return self.__products

    def has(self, name):
        if not list(filter(lambda product: product.name == name, self.__products)):
            raise Exception

    def get(self, name):
        for product in self.__products:
            if product.name == name:
                return product

        raise Exception()


class CashRegister:

    def __init__(self, warehouse: Warehouse) -> None:
        self.warehouse = warehouse
        self.orders = []
        self.sum = 0

    def order(self, name: str, quantity: int):
        self.warehouse.has(name)
        self.orders.append((name, quantity))

    def bill(self):
        products = []

        for order in self.orders:
            product = self.warehouse.get(order[0])
            self.sum += product.price * order[1]
            products.append((order[0], order[1], self.sum))

        return Bill(sum=self.sum, products=products)


class Bill:
    def __init__(self, sum: int, products: list) -> None:
        self.products = products
        self.sum = sum


class TestClass:
    def test_create_product(self):
        product = Product(name='Banana', unit='kg', price=499)

        assert product.name == 'Banana'
        assert product.unit == 'kg'
        assert product.price == 499

    def test_create_product_with_incorrect_unit(self):
        with pytest.raises(Exception):
            Product(name='Banana', unit='test', price=499)

    def test_create_product_without_unit(self):
        with pytest.raises(Exception):
            Product(name='Banana', price=499)

    def test_create_product_with_incorrect_price(self):
        with pytest.raises(Exception):
            Product(name='Banana', price=0)

        with pytest.raises(Exception):
            Product(name='Banana', price=-1)

    def test_add_product_to_warehouse(test):
        warehouse = Warehouse()
        warehouse.add(Product(name='Banana', unit='kg', price=499))

        assert 1 == len(warehouse.products())

    def test_get_product_from_warehouse_by_name(test):
        warehouse = Warehouse()
        warehouse.add(Product(name='Banana', unit='kg', price=499))

        assert 'Banana' == warehouse.get(name='Banana').name

    def test_raise_exception_when_product_not_found_in_warehouse(test):
        with pytest.raises(Exception):
            Warehouse().get('Avocado')

    def test_raise_exception_when_product_not_found_in_warehouse_using_has_method(test):
        with pytest.raises(Exception):
            Warehouse().has('Avocado')

    def test_order_two_kg_of_product_in_cash_register(self):
        warehouse = Warehouse()
        warehouse.add(Product(name='Banana', unit='kg', price=499))

        cash_register = CashRegister(warehouse)

        cash_register.order(name='Banana', quantity=2)

        assert 998 == cash_register.bill().sum

    def test_order_on_cash_register_and_return_bill(self):
        warehouse = Warehouse()
        warehouse.add(Product(name='Banana', unit='kg', price=499))

        cash_register = CashRegister(warehouse)

        cash_register.order(name='Banana', quantity=2)

        assert Bill == type(cash_register.bill())

    def test_order_two_kg_of_product_in_cash_register_and_check_bill(self):
        warehouse = Warehouse()
        warehouse.add(Product(name='Banana', unit='kg', price=499))

        cash_register = CashRegister(warehouse)

        cash_register.order(name='Banana', quantity=2)

        assert 1 == len(cash_register.bill().products)

    def test_order_two_different_product(self):
        warehouse = Warehouse()
        warehouse.add(Product(name='Tomatoes', unit='kg', price=1000))
        warehouse.add(Product(name='Avocado', unit='item', price=2000))

        cash_register = CashRegister(warehouse)

        cash_register.order(name='Tomatoes', quantity=2)
        cash_register.order(name='Avocado', quantity=2)

        bill = cash_register.bill()

        assert 2 == len(bill.products)
        assert 6000 == bill.sum

    def test_raise_exception_when_try_order_product_which_are_not_available(self):
        warehouse = Warehouse()
        warehouse.add(Product(name='Avocado', unit='item', price=2000))
        cash_register = CashRegister(warehouse)

        with pytest.raises(Exception):
            cash_register.order(name='Tomatoes', quantity=2)
