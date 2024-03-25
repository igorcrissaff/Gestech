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
@jwt.jwt_required()
@admin_required()
def add():
    try:
        db.session.add(User(**request.json))
        db.session.commit()
        return '', 204
    except Exception as erro:
        return abort(400, repr(erro))
##########################################################################

# Read
@usuarios.route('/get_all', methods=['GET'])
@admin_required()
@cache.cached()
def get_all():
    data = User.query.all()
    if data:
        users = [x.dict() for x in data]
        return jsonify(users)
    else:
        return 'No Products'
    
@usuarios.route('/get/<codigo>', methods=['GET'])
@admin_required()
def get(codigo):
    user = User.query.filter_by(id=codigo).first()
    if user:
        return jsonify(user.dict())
    else:
        return abort(400, 'Product Not Found')
    
@usuarios.route('/get/vendas/<codigo>')
@admin_required()
@cache.cached()
def get_vendas(codigo):
    usuario = User.query.filter_by(id=codigo).first()
    if usuario:
        data = usuario.vendas
        vendas = []
        for venda in data:
            vendas.append(venda.dict())
        return jsonify(vendas)
##########################################################################
    
# Update
@usuarios.route('/edit/<codigo>', methods=['PUT'])
@admin_required()
def edit(codigo):
    user = User.query.filter_by(id=codigo).first()
    if user:
        for key, value in request.json.items():
            setattr(user, key, value)
        db.session.commit()
        return ''
    else:
        return abort(400, 'User Not Found')
##########################################################################
    
# Delete
@usuarios.route('/delete/<codigo>', methods=['DELETE'])
@admin_required()
def delete(codigo):
    user = User.query.filter_by(id=codigo).first()
    if user:
        user.delete()
        db.session.commit()
        return '', 204
    else:
        return abort(400, "User Not Found")
##########################################################################
