from . import db
#from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(13), primary_key=True)
    name = db.Column(db.String(50) , nullable=False, unique=True)
    price = db.Column(db.Float(), nullable=False)
    quantity = db.Column(db.Float(), nullable=False, default=0)

    #_created_at = db.Column(db.DateTime(), default=datetime.now())
    #_updated_at = db.Column(db.DateTime())

    sales = db.relationship('Sale', backref='product')
    purchases = db.relationship('Purchase', backref='product')

    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
        #self._created_at = datetime.now()
        
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, quantity={self.quantity})>"

    @hybrid_property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }