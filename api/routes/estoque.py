#Setup
from flask import Blueprint, request, abort
import flask_jwt_extended as jwt

from ..extensions.jwt import admin_required
from ..extensions.cache import cache

from ..models import db
from ..models.produto import Produto

estoque = Blueprint('estoque', __name__)
##########################################################################

#Create
@estoque.route('/add', methods=["POST"])
@jwt.jwt_required()
@admin_required()
def add():
    db.session.add(Produto(**request.json))
    db.session.commit()
    return ''
##########################################################################

#Read
@estoque.route('/get_all', methods=['GET'])
@jwt.jwt_required()
@admin_required()
@cache.cached()
def get_all():
    json = request.get_json(silent=True)
    filtros = []
    if json:
        filtros = [getattr(Produto, attr) == value for attr, value in json.items()]

    data = Produto.query.filter(*filtros).all()
    produtos = []
    if data:
        for produto in data:
            produto = produto.__dict__
            produto.pop('_sa_instance_state')
            produtos.append(produto)
    return produtos

@estoque.route('/get/<codigo>', methods=['GET'])
@jwt.jwt_required()
def get(codigo):  
    produto = Produto.query.filter_by(id=codigo).first()
    if produto:
        produto = produto.__dict__
        produto.pop('_sa_instance_state')
        return produto
    else:
        return abort(400, 'Product Not Found')
    
@estoque.route('/get/vendas/<codigo>')
@jwt.jwt_required()
@admin_required()
def get_vendas(codigo):
    produto = Produto.query.filter_by(id=codigo).first()
    if produto:
        data = produto.vendas
        vendas = []
        for venda in data:
            venda = venda.__dict__
            venda.pop('_sa_instance_state')
            vendas.append(venda)
            vendas.clear()
        return vendas
    else:
        return abort(400, 'Product Not Found')

@estoque.route('/get/compras/<codigo>')
@jwt.jwt_required()
@admin_required()
def get_compras(codigo):
    produto = Produto.query.filter_by(id=codigo).first()
    if produto:
        data = produto.vendas
        compras = []
        for compra in data:
            compra = compra.__dict__
            compra.pop('_sa_instance_state')
            compras.append(compra)
        return compras
    else:
        return abort(400, 'Product Not Found')
##########################################################################
    
#Update
@estoque.route('/edit/<codigo>', methods=['PUT'])
@jwt.jwt_required()
def edit(codigo):
    produto = Produto.query.filter_by(id=codigo).first()
    if produto:
        for key, value in request.json.items():
            setattr(produto, key, value)
        db.session.commit()
        return '', 204
    else:
        return abort(400, 'Product Not Found')
##########################################################################
    
#Delete
@estoque.route('/delete/<codigo>', methods=['DELETE'])
@jwt.jwt_required()
@admin_required()
def delete(codigo):
    produto = Produto.query.filter_by(id=codigo).first()
    if produto:
        produto.delete()
        db.session.commit()
        return '', 204
    else:
        return abort(400, 'Product Not Found')
##########################################################################
