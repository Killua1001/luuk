# Arquivo: main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from database.database_manager import DatabaseManager
from modules.product_management import ProductManagementTab
from modules.sales_management import SalesManagementTab
from modules.inventory_management import InventoryManagementTab
from modules.reports_management import ReportsManagementTab

class InventoryManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestão de Estoque")
        self.setGeometry(100, 100, 1200, 800)

        # Inicializar o banco de dados
        self.db_manager = DatabaseManager()

        # Configurar layout principal
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Criar abas do sistema
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Adicionar abas de gerenciamento
        self.product_tab = ProductManagementTab(self.db_manager)
        self.sales_tab = SalesManagementTab(self.db_manager)
        self.inventory_tab = InventoryManagementTab(self.db_manager)
        self.reports_tab = ReportsManagementTab(self.db_manager)

        self.tab_widget.addTab(self.product_tab, "Produtos")
        self.tab_widget.addTab(self.sales_tab, "Vendas")
        self.tab_widget.addTab(self.inventory_tab, "Estoque")
        self.tab_widget.addTab(self.reports_tab, "Relatórios")

# database/database_manager.py
import sqlite3
import json
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='inventory.db'):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de Produtos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE NOT NULL,
                    nome TEXT NOT NULL,
                    preco REAL NOT NULL,
                    quantidade INTEGER NOT NULL,
                    nivel_minimo INTEGER NOT NULL
                )
            ''')

            # Tabela de Vendas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data DATETIME NOT NULL,
                    produto_id INTEGER NOT NULL,
                    quantidade INTEGER NOT NULL,
                    valor_total REAL NOT NULL,
                    FOREIGN KEY (produto_id) REFERENCES produtos(id)
                )
            ''')

            conn.commit()

    def adicionar_produto(self, codigo, nome, preco, quantidade, nivel_minimo):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO produtos (codigo, nome, preco, quantidade, nivel_minimo)
                VALUES (?, ?, ?, ?, ?)
            ''', (codigo, nome, preco, quantidade, nivel_minimo))
            conn.commit()
            return cursor.lastrowid

    def realizar_venda(self, produto_id, quantidade):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Verificar estoque disponível
            cursor.execute('SELECT quantidade, preco FROM produtos WHERE id = ?', (produto_id,))
            produto = cursor.fetchone()
            
            if not produto or produto[0] < quantidade:
                raise ValueError("Estoque insuficiente")

            # Atualizar estoque
            novo_estoque = produto[0] - quantidade
            cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (novo_estoque, produto_id))

            # Registrar venda
            valor_total = produto[1] * quantidade
            cursor.execute('''
                INSERT INTO vendas (data, produto_id, quantidade, valor_total)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now(), produto_id, quantidade, valor_total))
            
            conn.commit()
            return novo_estoque

    def exportar_vendas_json(self, data_inicial=None, data_final=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = '''
                SELECT v.id, v.data, p.nome, v.quantidade, v.valor_total
                FROM vendas v
                JOIN produtos p ON v.produto_id = p.id
            '''
            params = []

            if data_inicial and data_final:
                query += ' WHERE v.data BETWEEN ? AND ?'
                params = [data_inicial, data_final]

            cursor.execute(query, params)
            vendas = cursor.fetchall()

            vendas_dict = [
                {
                    'id': venda[0],
                    'data': venda[1],
                    'produto': venda[2],
                    'quantidade': venda[3],
                    'valor_total': venda[4]
                } for venda in vendas
            ]

            # Criar diretório de relatórios
            os.makedirs('relatorios', exist_ok=True)
            
            # Nome do arquivo com timestamp
            nome_arquivo = f'relatorios/vendas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            
            with open(nome_arquivo, 'w') as f:
                json.dump(vendas_dict, f, indent=4)

            return nome_arquivo

# modules/product_management.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QTableWidget, QTableWidgetItem, QPushButton, QMessageBox)

class ProductManagementTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Formulário de cadastro de produto
        form_layout = QHBoxLayout()
        
        self.cod_input = QLineEdit()
        self.cod_input.setPlaceholderText("Código")
        
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")
        
        self.preco_input = QLineEdit()
        self.preco_input.setPlaceholderText("Preço")
        
        self.quantidade_input = QLineEdit()
        self.quantidade_input.setPlaceholderText("Quantidade")
        
        self.nivel_minimo_input = QLineEdit()
        self.nivel_minimo_input.setPlaceholderText("Nível Mínimo")

        adicionar_btn = QPushButton("Adicionar Produto")
        adicionar_btn.clicked.connect(self.adicionar_produto)

        form_layout.addWidget(self.cod_input)
        form_layout.addWidget(self.nome_input)
        form_layout.addWidget(self.preco_input)
        form_layout.addWidget(self.quantidade_input)
        form_layout.addWidget(self.nivel_minimo_input)
        form_layout.addWidget(adicionar_btn)

        layout.addLayout(form_layout)

        # Tabela de produtos
        self.produtos_table = QTableWidget()
        self.produtos_table.setColumnCount(6)
        self.produtos_table.setHorizontalHeaderLabels(["ID", "Código", "Nome", "Preço", "Quantidade", "Nível Mínimo"])
        layout.addWidget(self.produtos_table)

        self.setLayout(layout)

    def adicionar_produto(self):
        try:
            codigo = self.cod_input.text()
            nome = self.nome_input.text()
            preco = float(self.preco_input.text())
            quantidade = int(self.quantidade_input.text())
            nivel_minimo = int(self.nivel_minimo_input.text())

            produto_id = self.db_manager.adicionar_produto(codigo, nome, preco, quantidade, nivel_minimo)
            
            QMessageBox.information(self, "Sucesso", "Produto adicionado com sucesso!")
            
            # Limpar inputs
            self.cod_input.clear()
            self.nome_input.clear()
            self.preco_input.clear()
            self.quantidade_input.clear()
            self.nivel_minimo_input.clear()

        except ValueError as e:
            QMessageBox.warning(self, "Erro", str(e))

# Outros módulos (sales_management.py, inventory_management.py, reports_management.py) 
# seriam desenvolvidos de forma similar, com suas respectivas funcionalidades

def main():
    app = QApplication(sys.argv)
    sistema = InventoryManagementSystem()
    sistema.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
