class Product:
    def __init__(self, id, name, code, price, quantity, reorder_level):
        self.id = id
        self.name = name
        self.code = code
        self.price = price
        self.quantity = quantity
        self.reorder_level = reorder_level

    def __str__(self):
        return f"Product(id={self.id}, name={self.name}, code={self.code}, price={self.price}, quantity={self.quantity}, reorder_level={self.reorder_level})"

print("Product module loaded successfully.")