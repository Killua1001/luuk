import json
from models import Database, Product, Sale

def display_menu():
    print("\n=== Inventory Management System ===")
    print("1. Add Product")
    print("2. View All Products")
    print("3. Make Sale")
    print("4. Check Low Stock")
    print("5. Export Sales Report")
    print("6. Exit")
    return input("Select an option: ")

def main():
    db = Database()
    product_manager = Product(db)
    sale_manager = Sale(db)
    
    while True:
        choice = display_menu()
        
        if choice == "1":
            code = input("Enter product code: ")
            name = input("Enter product name: ")
            price = float(input("Enter price: "))
            quantity = int(input("Enter quantity: "))
            min_quantity = int(input("Enter minimum quantity: "))
            
            try:
                product_manager.add_product(code, name, price, quantity, min_quantity)
                print("Product added successfully!")
            except Exception as e:
                print(f"Error adding product: {e}")
        
        elif choice == "2":
            products = product_manager.get_all_products()
            print("\nCurrent Inventory:")
            print("ID | Code | Name | Price | Quantity | Min Quantity")
            print("-" * 50)
            for product in products:
                print(f"{product[0]} | {product[1]} | {product[2]} | ${product[3]} | {product[4]} | {product[5]}")
        
        elif choice == "3":
            code = input("Enter product code: ")
            quantity = int(input("Enter quantity to sell: "))
            
            success, message = sale_manager.make_sale(code, quantity)
            print(message)
        
        elif choice == "4":
            low_stock = product_manager.check_low_stock()
            print("\nLow Stock Products:")
            for product in low_stock:
                print(f"Code: {product[1]}, Name: {product[2]}, Current Quantity: {product[4]}, Min Quantity: {product[5]}")
        
        elif choice == "5":
            cursor = db.conn.cursor()
            cursor.execute('''
                SELECT s.date, p.code, p.name, s.quantity, s.total_price 
                FROM sales s 
                JOIN products p ON s.product_id = p.id
            ''')
            sales = cursor.fetchall()
            
            sales_report = []
            for sale in sales:
                sales_report.append({
                    "date": sale[0],
                    "product_code": sale[1],
                    "product_name": sale[2],
                    "quantity": sale[3],
                    "total_price": sale[4]
                })
            
            with open("sales_report.json", "w") as f:
                json.dump(sales_report, f, indent=2)
            print("Sales report exported to sales_report.json")
        
        elif choice == "6":
            print("Thank you for using the Inventory Management System!")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()