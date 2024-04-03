from . import db
from .product import Product
from .user import User
from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property

class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer(), primary_key=True)

    product_id = db.Column(db.String(13), db.ForeignKey('products.id'), nullable=False)
    seller_id = db.Column(db.String(11), db.ForeignKey('users.id'), nullable=False)

    quantity = db.Column(db.Integer(), nullable=False)
    value = db.Column(db.Float(), nullable=False)

    

    date = db.Column(db.Date(), nullable=False, default=date.today())

    def __init__(self, seller_id, product_id, quantity, date=None,):
        self.product_id = product_id
        self.seller_id = seller_id
        
        self.quantity = quantity
        self.price = self.product.price * quantity

        self.date = date

    def __repr__(self) -> str:
        return f"<Sale() id={self.id}, seller{repr(self.seller)}, product={repr(self.product)}, quantity={self.quantity}, price={self.price}, date={self.date}>"

    @hybrid_property
    def dict(self):
        return {
            "id": self.id,
            "seller": self.seller.dict,
            "product": self.product.dict,
            "quantity": self.quantity,
            "price": self.price,
            "date": self.date
        }
    
    @hybrid_property
    def product(self):
        return Product.query.get(self.product_id)
    
    @hybrid_property
    def seller(self):
        return User.query.get(self.seller_id)