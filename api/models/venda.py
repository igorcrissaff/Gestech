from . import db
from .produto import Produto
from datetime import date

class Venda(db.Model):
    __tablename__ = 'vendas'

    venda = db.Column(db.Integer(), primary_key=True)
    quantidade = db.Column(db.Integer(), nullable=False)
    valor = db.Column(db.Float(), nullable=False)
    pgto = db.Column(db.String(30), nullable=False)
    data = db.Column(db.Date(), nullable=False, default=date.today())

    id_produto = db.Column(db.String(13), db.ForeignKey('produtos.id'), nullable=False)
    id_vendedor = db.Column(db.String(4), db.ForeignKey('usuarios.id'), nullable=False)
    
    
    def __init__(self, id_produto, id_vendedor, quantidade, pgto, data=date.today()):
        self.id_produto = id_produto
        self.id_vendedor = id_vendedor
        self.quantidade = quantidade
        self.valor = Produto.query.filter_by(id=id_produto).first().valor * quantidade
        self.pgto = pgto
        
        ano, mes, dia = data.split('-')
        self.data = date(int(ano), int(mes), int(dia))
