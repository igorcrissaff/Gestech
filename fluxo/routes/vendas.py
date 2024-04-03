#Setup
from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required

from ..extensions.jwt import admin_required

from ..models import db
from ..models.sale import Sale
from ..models.product import Product

vendas = Blueprint('venda', __name__)
##########################################################################

#Create
@vendas.route('/add', methods=["POST"])
@jwt_required()
def add():
    produto = Product.query.filter_by(id=request.json['id_produto']).first()
    if produto:
        db.session.add(Sale(**request.json))
        produto.estoque -= request.json['quantidade']
        db.session.commit()    
        return 'OK'
    else:
        return 'Product Not Found', 400
##########################################################################

#Read
@vendas.route('/get_all', methods=['GET'])
@admin_required()
def get_all():
    vendas = Sale.query.all()
    if vendas:
        vendas = [x.dict for x in vendas]
    return vendas
    

@vendas.route('/get/<codigo>', methods=['GET'])
@admin_required()
def get(codigo):  
    venda = Sale.query.get(codigo)
    if venda: 
        return venda.dict
    else:
        return abort(400, 'Sale Not Found')
     
##########################################################################
