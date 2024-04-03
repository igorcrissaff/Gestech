#Setup
from flask import Blueprint, request, abort, jsonify
import flask_jwt_extended as jwt

from ..extensions.jwt import admin_required
from ..extensions.cache import cache

from ..models import db
from ..models.user import User

usuarios = Blueprint('usuarios', __name__)
##########################################################################

# Create
@usuarios.route('/add', methods=["POST"])
#@admin_required()
def add():
    try:
        user = User(**request.json)
        db.session.add(user)
        db.session.commit()
        return '', 204
    except Exception as erro:
        return abort(400, repr(erro))
##########################################################################

# Read
@usuarios.route('/get_all', methods=['GET'])
@admin_required()
#@cache.cached()
def get_all():
    data = User.query.all()
    if data:
        users = [x.dict for x in data]
        return jsonify(users)
    else:
        return 'No Users Found'
    
@usuarios.route('/get/<codigo>', methods=['GET'])
@admin_required()
def get(codigo):
    user = User.query.get(codigo)
    if user:
        return user.dict
    else:
        return abort(400, 'Product Not Found')
    
@usuarios.route('/get/vendas/<codigo>')
@admin_required()
#@cache.cached()
def get_vendas(codigo):
    usuario = User.query.get(codigo)
    if usuario:
        data = usuario.sales
        vendas = []
        for venda in data:
            vendas.append(venda.dict)
        return jsonify(vendas)
##########################################################################
    
# Update
@usuarios.route('/edit/<codigo>', methods=['PUT'])
@admin_required()
def edit(codigo):
    user = User.query.get(codigo)
    if user:
        for key, value in request.json.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return '', 204
    else:
        return abort(400, 'User Not Found')
##########################################################################
    
# Delete
@usuarios.route('/delete/<codigo>', methods=['DELETE'])
@admin_required()
def delete(codigo):
    user = User.query.get(codigo)
    if user:
        user.delete()
        db.session.commit()
        return '', 204
    else:
        return abort(400, "User Not Found")
##########################################################################
