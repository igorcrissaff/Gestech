from . import db
from .produto import Produto
from datetime import date

class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer(), primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False)
    value = db.Column(db.Float(), nullable=False)
    date = db.Column(db.Date(), nullable=False, default=date.today())

    product_id = db.Column(db.String(13), db.ForeignKey('products.id'), nullable=False)
    seller_id = db.Column(db.String(4), db.ForeignKey('users.id'), nullable=False)
    
    
    def __init__(self, id_produto, id_vendedor, quantidade, pgto, data=None):
        self.id_produto = id_produto
        self.id_vendedor = id_vendedor
        self.quantidade = quantidade
        self.valor = Produto.query.filter_by(id=id_produto).first().valor * quantidade
        self.pgto = pgto
        

        self.data = date(data)

    def dict(self):
        venda = self.__dict__
        venda.pop('_sa_instance_state')
        return venda