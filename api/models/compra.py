from . import db
from datetime import date

class Compra(db.Model):
    __tablename__ = 'compras'

    compra = db.Column(db.Integer(), primary_key=True)
    id_produto = db.Column(db.String(13), db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer(), nullable=False)
    valor = db.Column(db.Float(), nullable=False)
    data = db.Column(db.Date(), nullable=False, default=date.today())
    
    def __init__(self, id_produto, quantidade, valor, data=date.today()):
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.valor = valor
        self.data = data
