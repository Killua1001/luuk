from database import Database

class Sales:
    def __init__(self):
        self.db = Database()

    def make_sale(self, product_code, quantity):
        product = self.db.get_product_by_code(product_code)
        if not product:
            raise ValueError("Product not found")
        
        if product[4] < quantity:
            raise ValueError("Insufficient stock")
        
        total_value = product[3] * quantity
        self.db.add_sale(product[0], quantity, total_value)
        new_quantity = product[4] - quantity
        self.db.update_product_quantity(product[0], new_quantity)
        return total_value

    def get_sales_report(self):
        return self.db.get_sales_report()

    def export_sales_to_json(self, filename):
        self.db.export_sales_to_json(filename)

print("Sales module loaded successfully.")