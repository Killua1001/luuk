import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_name='inventory.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                reorder_level INTEGER NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                total_value REAL NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        self.conn.commit()

    def add_product(self, name, code, price, quantity, reorder_level):
        self.cursor.execute('''
            INSERT INTO products (name, code, price, quantity, reorder_level)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, code, price, quantity, reorder_level))
        self.conn.commit()

    def update_product_quantity(self, product_id, new_quantity):
        self.cursor.execute('''
            UPDATE products SET quantity = ? WHERE id = ?
        ''', (new_quantity, product_id))
        self.conn.commit()

    def get_all_products(self):
        self.cursor.execute('SELECT * FROM products')
        return self.cursor.fetchall()

    def get_product_by_code(self, code):
        self.cursor.execute('SELECT * FROM products WHERE code = ?', (code,))
        return self.cursor.fetchone()

    def add_sale(self, product_id, quantity, total_value):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO sales (date, product_id, quantity, total_value)
            VALUES (?, ?, ?, ?)
        ''', (date, product_id, quantity, total_value))
        self.conn.commit()

    def get_sales_report(self):
        self.cursor.execute('''
            SELECT s.date, p.name, s.quantity, s.total_value
            FROM sales s
            JOIN products p ON s.product_id = p.id
        ''')
        return self.cursor.fetchall()

    def export_sales_to_json(self, filename):
        sales = self.get_sales_report()
        sales_data = [
            {
                "date": sale[0],
                "product": sale[1],
                "quantity": sale[2],
                "total_value": sale[3]
            }
            for sale in sales
        ]
        with open(filename, 'w') as f:
            json.dump(sales_data, f, indent=4)

    def close(self):
        self.conn.close()

print("Database module loaded successfully.")