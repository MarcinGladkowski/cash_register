from test_main import Warehouse, Product, CashRegister

warehouse = Warehouse()
warehouse.add(Product(name='Banana', unit='kg', price=499))

cash_register = CashRegister(warehouse)

product_name = input('Choose product by name, please\n')

if not product_name:
    raise Exception

product = warehouse.get(product_name)

product_quantity = input('Choose quantity of product, please\n')

cash_register.order(name=product_name, quantity=int(product_quantity))

sum = cash_register.sum()

print(sum)