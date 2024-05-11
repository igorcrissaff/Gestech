#Setup
from flask_restful import Resource, request, abort
from flask_jwt_extended import jwt_required

from ..extensions.jwt import admin_required

from ..models import db
from ..models.sale import Sale
from ..models.product import Product


class Sales(Resource):

    @admin_required()
    def get(self):
        args = request.args
        filters = ['']
        for attr, value in args.items():
            attr = attr.replace('_','.') if '_' in attr else attr
            if hasattr(Sale, attr):
                filters.append(getattr(Sale, attr) == value)
            
        sales = Sale.query.filter(*filters).all()
        if sales:
            sales = [sale.dict() for sale in sales]
            return sales
        else:
            return 'None'
    
    @jwt_required()
    def post(self):
        product_id = request.json.get('product_id')
        if not product_id:
            return abort(400, message='Missing id')
        product = Product.query.get(product_id)
        if not product:
            return abort(400, message='Product Not Found')
    
        db.session.add(Sale(**request.json))
        product.quantity -= request.json['quantity']
        db.session.commit()    
        return 'OK'
