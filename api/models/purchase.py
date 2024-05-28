from . import db
from .product import Product
from datetime import date as Date
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

class Purchase(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer(), primary_key=True)
    product_id = db.Column(db.String(13), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Float(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    date = db.Column(db.Date(), nullable=False, default=Date.today())
    
    def __init__(self, product_id, quantity, price, date=None):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        print(date)
        self.date = datetime.strptime(date, '%dd-%mm-%YYYY') 

    def dict(self):
        return {
            "id": self.id,
            "product": self.product.dict,
            "quantity": self.quantity,
            "price": self.price,
            "date": self.date
        }
    
    @hybrid_property
    def product(self):
        return Product.query.get(self.product_id)
    

