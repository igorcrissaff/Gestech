from flask_restful import Resource, request, abort
from flask_jwt_extended import jwt_required
from datetime import datetime

from ..extensions.jwt import admin_required

from ..models import db
from ..models.purchase import Purchase
from ..models.product import Product


class Purchases(Resource):
    @admin_required()
    def get(self):
        args = request.args
        filters = []
        for attr, value in args.items():
            attr = attr.replace('_','.') if '_' in attr else attr
            if hasattr(Purchase, attr):
                filters.append(getattr(Purchase, attr) == value)
            elif attr == 'start.date':
                print(datetime.strptime(value, '%Y-%m-%d'))
                filters.append(Purchase.date >= datetime.strptime(value, '%Y-%m-%d'))
            elif attr == 'end.date':
                filters.append(Purchase.date <= datetime.strptime(value, '%Y-%m-%d'))
            
        purchases = Purchase.query.filter(*filters).all()
        if purchases:
            purchases = [purchase.dict() for purchase in purchases]
            return purchases
        else:
            return 'None'
        
    @jwt_required()
    def post(self):
        data = request.json
        if not data:
            return abort(400, status='400 Bad Request', msg='missing request body')

        product_id = request.json.get('product_id')
        if not product_id:
            return abort(400, message='Missing id')
        product = Product.query.get(product_id)
        if not product:
            return abort(400, message='Product Not Found')
        
        


        db.session.add(Purchase(**request.json))
        product.quantity += request.json['quantity']
        db.session.commit()    
        return 'OK'
    
