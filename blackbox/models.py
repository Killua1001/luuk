class Produto:
    def __init__(self, nome, codigo, preco, quantidade):
        self.nome = nome
        self.codigo = codigo
        self.preco = preco
        self.quantidade = quantidade

class Venda:
    def __init__(self, produto_id, quantidade, valor_total):
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.valor_total = valor_total