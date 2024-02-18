#Setup
from flask import Blueprint, request, abort
import flask_jwt_extended as jwt

from ..models import db
from ..models.produto import Produto

estoque = Blueprint('estoque', __name__)
##########################################################################

#Create
@estoque.route('/add', methods=["POST"])
@jwt.jwt_required()
def add():
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        db.session.add(Produto(request.json))
        db.session.commit()
        return ''
    else:
        return abort(401)
##########################################################################

#Read
@estoque.route('/get_all', methods=['GET'])
@jwt.jwt_required()
def get_all():
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        data = Produto.query.all()
        produtos = []
        for produto in data:
            produto = produto.__dict__
            produto.pop('_sa_instance_state')
            produtos.append(produto)
        return produtos
    else:
        return abort(401)

@estoque.route('/get/<codigo>', methods=['GET'])
@jwt.jwt_required()
def get(codigo):  
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        produto = Produto.query.filter_by(id=codigo).first()
        if produto:
            produto = produto.__dict__
            produto.pop('_sa_instance_state')
            return produto
        else:
            return abort(400, 'Product Not Found')
    else:
        return abort(401)
    
@estoque.route('/get/vendas/<codigo>')
@jwt.jwt_required()
def get_vendas(codigo):
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        produto = Produto.query.filter_by(id=codigo).first()
        if produto:
            data = produto.vendas
            vendas = []
            for venda in data:
                venda = venda.__dict__
                venda.pop('_sa_instance_state')
                vendas.append(venda)
            return vendas
        else:
            return abort(400, 'Product Not Found')
    else:
        return abort(401)

@estoque.route('/get/compras/<codigo>')
@jwt.jwt_required()
def get_compras(codigo):
    user = jwt.get_current_user()
    if user.cargo == 'admin':
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
    else:
        return abort(401)
##########################################################################
    
#Update
@estoque.route('/edit/<codigo>', methods=['PUT'])
@jwt.jwt_required()
def edit(codigo):
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        produto = Produto.query.filter_by(id=codigo).first()
        if produto:
            for key, value in request.json.items():
                setattr(produto, key, value)
            db.session.commit()
            return ''
        else:
            return abort(400, 'Product Not Found')
    else:
        return abort(401)
##########################################################################
    
#Delete
@estoque.route('/delete/<codigo>', methods=['DELETE'])
@jwt.jwt_required()
def delete(codigo):
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        Produto.query.filter_by(id=codigo).delete()
        db.session.commit()
        return ''
    else:
        return abort(401)
##########################################################################
