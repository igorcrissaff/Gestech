from . import db
from datetime import datetime

class Compra(db.Model):
    __tablename__ = 'compras'

    compra = db.Column(db.Integer(), primary_key=True)
    id_produto = db.Column(db.String(13), db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer(), nullable=False)
    valor = db.Column(db.Float(), nullable=False)
    data = db.Column(db.DateTime(), nullable=False)
    
    def __init__(self, data):
        self.id_produto = data['id_produto']
        self.quantidade = data['quantidade']
        self.valor = data['valor']
        self.data = datetime.now()
