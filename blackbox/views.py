import tkinter as tk
from tkinter import messagebox, simpledialog
from controllers import cadastrar_produto, realizar_venda, gerar_relatorio_vendas
from models import Produto

def cadastrar_produto_view():
    nome = simpledialog.askstring("Cadastro de Produto", "Nome do Produto:")
    codigo = simpledialog.askstring("Cadastro de Produto", "Código do Produto:")
    preco = simpledialog.askfloat("Cadastro de Produto", "Preço do Produto:")
    quantidade = simpledialog.askinteger("Cadastro de Produto", "Quantidade em Estoque:")
    
    if nome and codigo and preco is not None and quantidade is not None:
        produto = Produto(nome, codigo, preco, quantidade)
        cadastrar_produto(produto)
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
    else:
        messagebox.showwarning("Erro", "Todos os campos devem ser preenchidos.")

def realizar_venda_view():
    produto_id = simpledialog.askinteger("Venda", "ID do Produto:")
    quantidade = simpledialog.askinteger("Venda", "Quantidade a Vender:")
    
    if produto