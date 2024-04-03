#Setup
from flask import Blueprint, request, abort, jsonify
import flask_jwt_extended as jwt

from ..extensions.jwt import admin_required
#from ..extensions.cache import cache

from ..models import db
from ..models.product import Product

estoque = Blueprint('estoque', __name__)
##########################################################################

#Create
@estoque.route('/add', methods=["POST"])
@jwt.jwt_required()
#@admin_required()
def add():
    try:
        db.session.add(Product(**request.json))
        db.session.commit()
        return ''
    except Exception as error:
        return abort(400, repr(error))
##########################################################################

#Read
@estoque.route('/get_all', methods=['GET'])
@admin_required()
#@cache.cached()
def get_all():
    json = request.get_json(silent=True)
    filtros = []
    if json:
        filtros = [getattr(Product, attr) == value for attr, value in json.items()]

    data = Product.query.filter(*filtros).all()
    produtos = []
    if data:
        produtos = [produto.dict for produto in data]
    return produtos

@estoque.route('/get/<codigo>', methods=['GET'])
@jwt.jwt_required()
def get(codigo):  
    produto = Product.query.get(codigo)
    if produto:
        return produto.dict
    else:
        return abort(400, 'Product Not Found')
    
@estoque.route('/get/vendas/<codigo>')
@admin_required()
def get_vendas(codigo):
    produto = Product.query.get(codigo)
    if produto:
        vendas = [venda.dict for venda in produto.sales]
        return vendas
    else:
        return abort(400, 'Product Not Found')

@estoque.route('/get/compras/<codigo>')
@admin_required()
def get_compras(codigo):
    produto = Product.query.get(codigo)
    if produto:
        compras = [compra.dict for compra in produto.purchases]
        return compras
    else:
        return abort(400, 'Product Not Found')
##########################################################################
    
#Update
@estoque.route('/edit/<codigo>', methods=['PUT'])
@admin_required()
def edit(codigo):
    produto = Product.query.filter_by(id=codigo).first()
    if produto:
        try:
            for key, value in request.json.items():
                if hasattr(produto, key):
                    setattr(produto, key, value)
            db.session.commit()
            return '', 204
        except Exception as error:
            return abort(400, repr(error))
    else:
        return abort(400, 'Product Not Found')
##########################################################################
    
#Delete
@estoque.route('/delete/<codigo>', methods=['DELETE'])
@admin_required()
def delete(codigo):
    produto = Product.query.filter_by(id=codigo).first()
    if produto:
        produto.delete()
        db.session.commit()
        return '', 204
    else:
        return abort(400, 'Product Not Found')
##########################################################################
