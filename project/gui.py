import tkinter as tk
from tkinter import ttk, messagebox
from inventory import Inventory
from sales import Sales

class InventoryGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Gestão de Estoque")
        self.inventory = Inventory()
        self.sales = Sales()

        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.master)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Products tab
        products_frame = ttk.Frame(notebook)
        notebook.add(products_frame, text="Produtos")
        self.create_products_tab(products_frame)

        # Sales tab
        sales_frame = ttk.Frame(notebook)
        notebook.add(sales_frame, text="Vendas")
        self.create_sales_tab(sales_frame)

        # Reports tab
        reports_frame = ttk.Frame(notebook)
        notebook.add(reports_frame, text="Relatórios")
        self.create_reports_tab(reports_frame)

    def create_products_tab(self, parent):
        # Add product form
        add_frame = ttk.LabelFrame(parent, text="Adicionar Produto")
        add_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(add_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(add_frame)
        self.name_entry.grid(row=0, column=1)

        ttk.Label(add_frame, text="Código:").grid(row=1, column=0, sticky=tk.W)
        self.code_entry = ttk.Entry(add_frame)
        self.code_entry.grid(row=1, column=1)

        ttk.Label(add_frame, text="Preço:").grid(row=2, column=0, sticky=tk.W)
        self.price_entry = ttk.Entry(add_frame)
        self.price_entry.grid(row=2, column=1)

        ttk.Label(add_frame, text="Quantidade:").grid(row=3, column=0, sticky=tk.W)
        self.quantity_entry = ttk.Entry(add_frame)
        self.quantity_entry.grid(row=3, column=1)

        ttk.Label(add_frame, text="Nível de Reposição:").grid(row=4, column=0, sticky=tk.W)
        self.reorder_entry = ttk.Entry(add_frame)
        self.reorder_entry.grid(row=4, column=1)

        ttk.Button(add_frame, text="Adicionar", command=self.add_product).grid(row=5, column=0, columnspan=2)

        # Product list
        list_frame = ttk.LabelFrame(parent, text="Lista de Produtos")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(list_frame, columns=("name", "code", "price", "quantity", "reorder"), show="headings")
        self.tree.heading("name", text="Nome")
        self.tree.heading("code", text="Código")
        self.tree.heading("price", text="Preço")
        self.tree.heading("quantity", text="Quantidade")
        self.tree.heading("reorder", text="Nível de Reposição")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.update_product_list()

    def create_sales_tab(self, parent):
        # Make sale form
        sale_frame = ttk.LabelFrame(parent, text="Realizar Venda")
        sale_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(sale_frame, text="Código do Produto:").grid(row=0, column=0, sticky=tk.W)
        self.sale_code_entry = ttk.Entry(sale_frame)
        self.sale_code_entry.grid(row=0, column=1)

        ttk.Label(sale_frame, text="Quantidade:").grid(row=1, column=0, sticky=tk.W)
        self.sale_quantity_entry = ttk.Entry(sale_frame)
        self.sale_quantity_entry.grid(row=1, column=1)

        ttk.Button(sale_frame, text="Realizar Venda", command=self.make_sale).grid(row=2, column=0, columnspan=2)

    def create_reports_tab(self, parent):
        ttk.Button(parent, text="Exportar Relatório de Vendas (JSON)", command=self.export_sales_report).pack(pady=10)

    def add_product(self):
        try:
            name = self.name_entry.get()
            code = self.code_entry.get()
            price = float(self.price_entry.get())
            quantity = int(self.quantity_entry.get())
            reorder_level = int(self.reorder_entry.get())

            self.inventory.add_product(name, code, price, quantity, reorder_level)
            self.update_product_list()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def make_sale(self):
        try:
            code = self.sale_code_entry.get()
            quantity = int(self.sale_quantity_entry.get())

            total_value = self.sales.make_sale(code, quantity)
            self.update_product_list()
            messagebox.showinfo("Sucesso", f"Venda realizada com sucesso! Valor total: R${total_value:.2f}")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    def update_product_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for product in self.inventory.get_all_products():
            self.tree.insert("", tk.END, values=(product.name, product.code, f"R${product.price:.2f}", product.quantity, product.reorder_level))

        self.check_low_stock()

    def check_low_stock(self):
        low_stock_products = self.inventory.check_low_stock()
        if low_stock_products:
            message = "Os seguintes produtos estão com estoque baixo:\n\n"
            for product in low_stock_products:
                message += f"{product.name} (Código: {product.code}): {product.quantity} unidades\n"
            messagebox.showwarning("Estoque Baixo", message)

    def export_sales_report(self):
        filename = "sales_report.json"
        self.sales.export_sales_to_json(filename)
        messagebox.showinfo("Sucesso", f"Relatório de vendas exportado para {filename}")

print("GUI module loaded successfully.")