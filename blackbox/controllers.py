from database import connect_db
from models import Produto, Venda
import json
from datetime import datetime

def cadastrar_produto(produto):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO produtos (nome, codigo, preco, quantidade)
        VALUES (?, ?, ?, ?)
    ''', (produto.nome, produto.codigo, produto.preco, produto.quantidade))
    conn.commit()
    conn.close()

def realizar_venda(produto_id, quantidade):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT preco, quantidade FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    
    if produto and produto[1] >= quantidade:
        valor_total = produto[0] * quantidade
        cursor.execute('''
            INSERT INTO vendas (data, produto_id, quantidade, valor_total)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), produto_id, quantidade, valor_total))
        
        cursor.execute('UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?', (quantidade, produto_id))
        conn.commit()
    conn.close()

def gerar_relatorio_vendas():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vendas')
    vendas = cursor.fetchall()
    conn.close()
    
    relatorio = []
    for venda in vendas:
        relatorio.append({
            'id': venda[0],
            'data': venda[1],
            'produto_id': venda[2],
            'quantidade': venda[3],
            'valor_total': venda[4]
        })
    
    with open('relatorio_vendas.json', 'w') as f:
        json.dump(relatorio, f)