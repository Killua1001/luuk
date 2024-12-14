import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('inventory.db')
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                code TEXT UNIQUE,
                name TEXT,
                price REAL,
                quantity INTEGER,
                min_quantity INTEGER
            )
        ''')
        
        # Sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                date TEXT,
                product_id INTEGER,
                quantity INTEGER,
                total_price REAL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        self.conn.commit()

class Product:
    def __init__(self, db):
        self.db = db
    
    def add_product(self, code, name, price, quantity, min_quantity):
        cursor = self.db.conn.cursor()
        cursor.execute('''
            INSERT INTO products (code, name, price, quantity, min_quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (code, name, price, quantity, min_quantity))
        self.db.conn.commit()
    
    def update_quantity(self, code, quantity):
        cursor = self.db.conn.cursor()
        cursor.execute('''
            UPDATE products 
            SET quantity = quantity + ? 
            WHERE code = ?
        ''', (quantity, code))
        self.db.conn.commit()
    
    def get_product(self, code):
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM products WHERE code = ?', (code,))
        return cursor.fetchone()
    
    def get_all_products(self):
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM products')
        return cursor.fetchall()
    
    def check_low_stock(self):
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT * FROM products 
            WHERE quantity <= min_quantity
        ''')
        return cursor.fetchall()

class Sale:
    def __init__(self, db):
        self.db = db
    
    def make_sale(self, product_code, quantity):
        cursor = self.db.conn.cursor()
        product = Product(self.db).get_product(product_code)
        
        if not product:
            return False, "Product not found"
        
        if product[4] < quantity:
            return False, "Insufficient stock"
        
        total_price = product[3] * quantity
        
        # Update product quantity
        cursor.execute('''
            UPDATE products 
            SET quantity = quantity - ? 
            WHERE code = ?
        ''', (quantity, product_code))
        
        # Record sale
        cursor.execute('''
            INSERT INTO sales (date, product_id, quantity, total_price)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), product[0], quantity, total_price))
        
        self.db.conn.commit()
        return True, "Sale completed successfully"