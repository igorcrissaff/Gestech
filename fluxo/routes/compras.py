#Setup
from flask import Blueprint, request, abort
#from flask_jwt_extended import jwt_required

from ..extensions.jwt import admin_required

from ..models import db
from ..models.purchase import Purchase
from ..models.product import Product

compras = Blueprint('compras', __name__)
##########################################################################

#Create
@compras.route('/add', methods=["POST"])
@admin_required()
def add():
    produto = Product.query.get(request.json['id_produto'])
    if produto:
        db.session.add(Purchase(**request.json))
        produto.estoque += request.json['quantidade']
        db.session.commit()
        return 'OK'
    else:
        return abort(400, 'Product Not Found')
##########################################################################

#Read
@compras.route('/get_all', methods=['GET'])
@admin_required()
def get_all():
    compras = Purchase.query.all()
    if compras:
        compras = [x.dict for x in compras]
    return compras

@compras.route('/get/<codigo>', methods=['GET'])
@admin_required()
def get(codigo):  
    compra = Purchase.query.get(codigo)
    if compra:
        return compra.dict
    else:
        return abort(400, 'Purchase Not Found')
##########################################################################
