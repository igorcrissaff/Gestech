#Setup
from flask_restful import Resource, request, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from ..extensions.jwt import admin_required
#from ..extensions.cache import cache

from ..models import db
from ..models.product import Product


class Stock(Resource):

    @jwt_required()
    def get(self):
        args = request.args
        filters = []
        for attr, value in args.items():
            if hasattr(Product, attr):
                filters.append(getattr(Product, attr) == value)

        products = Product.query.filter(*filters).all()
        if products:
            products = [product.dict for product in products]
            return products
        else:
            return 'None'

    @admin_required()
    def post(self):
        try:
            product = Product(**request.json)
            db.session.add(product)
            db.session.commit()
            return 'Product Posted'
        except IntegrityError:
            return abort(400, message='Product Already Registered')
        
    @admin_required()
    def patch(self):
        product_id = request.args.get('id')
        if not product_id:
            return abort(400, message='No Id Informed')
        
        product = Product.query.get(product_id)
        if not product:
            return abort(400, message='Product Not Found')
       
        try:
            for key, value in request.json.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            db.session.commit()
            return 'Product Patched'
        except IntegrityError:
            return abort(400, message='Product Name Already In Use')
            
    
    @admin_required()
    def delete(self):
        product_id = request.args.get('id')
        if not product_id:
            return abort(400, message='Missing Id')
        product = Product.query.get(product_id)
        if not product:
            return abort(400, message='Product Not Found')
    
        db.session.delete(product)
        db.session.commit()
        return 'Product Deleted'
