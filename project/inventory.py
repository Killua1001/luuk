from database import Database
from product import Product

class Inventory:
    def __init__(self):
        self.db = Database()

    def add_product(self, name, code, price, quantity, reorder_level):
        self.db.add_product(name, code, price, quantity, reorder_level)

    def update_product_quantity(self, product_id, new_quantity):
        self.db.update_product_quantity(product_id, new_quantity)

    def get_all_products(self):
        products_data = self.db.get_all_products()
        return [Product(*product) for product in products_data]

    def get_product_by_code(self, code):
        product_data = self.db.get_product_by_code(code)
        if product_data:
            return Product(*product_data)
        return None

    def check_low_stock(self):
        low_stock_products = []
        for product in self.get_all_products():
            if product.quantity < product.reorder_level:
                low_stock_products.append(product)
        return low_stock_products

print("Inventory module loaded successfully.")