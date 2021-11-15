from test_main import Warehouse, Product, CashRegister
import os

warehouse = Warehouse()
warehouse.add(Product(name='banana', unit='kg', price=49900))
warehouse.add(Product(name='avocado', unit='item', price=20000))

cash_register = CashRegister(warehouse)

while True:
    product_name = input('Choose product by name or finish (f), please\n')

    if product_name == 'f':
        bill = cash_register.bill()

        for i, order_product in enumerate(bill.products):
            print(f"{i}: product: {order_product[0]} - quantity: {order_product[1]} - sum: {order_product[2]/100:.2f}")

        print(f"bill summarize: {bill.sum/100:.2f}")
        break

    if not product_name:
        raise Exception

    product = warehouse.get(product_name.lower())

    product_quantity = input('Choose quantity of product, please\n')

    cash_register.order(name=product_name, quantity=int(product_quantity))

    clear = lambda: os.system('clear')
    clear()
