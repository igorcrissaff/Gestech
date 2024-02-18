from . import db
from .produto import Produto
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'vendas'

    venda = db.Column(db.Integer(), primary_key=True)
    quantidade = db.Column(db.Integer(), nullable=False)
    valor = db.Column(db.Float(), nullable=False)
    pgto = db.Column(db.String(30), nullable=False)
    data = db.Column(db.DateTime(), nullable=False)

    id_produto = db.Column(db.String(13), db.ForeignKey('produtos.id'), nullable=False)
    id_vendedor = db.Column(db.String(4), db.ForeignKey('usuarios.id'), nullable=False)
    
    
    def __init__(self, data):
        self.id_produto = data['id_produto']
        self.id_vendedor = data['id_vendedor']
        self.quantidade = data['quantidade']
        self.valor = Produto.query.filter_by(id=data['id_produto']).first().valor * data['quantidade']
        self.pgto = data['pgto']
        self.data = datetime.now()
