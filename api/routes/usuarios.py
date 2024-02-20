#Setup
from flask import Blueprint, request, abort, jsonify
import flask_jwt_extended as jwt

from ..extensions.jwt import admin_required

from ..models import db
from ..models.user import User

usuarios = Blueprint('usuarios', __name__)
##########################################################################

#Create
@usuarios.route('/add', methods=["POST"])
@jwt.jwt_required()
@admin_required()
def add():
    db.session.add(User(request.json))
    db.session.commit()
    return ''
##########################################################################

#Read
@usuarios.route('/get_all', methods=['GET'])
@jwt.jwt_required()
@admin_required()
def get_all():
    data = User.query.all()
    users = []
    for user in data:
        user = user.__dict__
        user.pop('_sa_instance_state')
        users.append(user)
    return jsonify(users)
    
@usuarios.route('/get/<codigo>', methods=['GET'])
@jwt.jwt_required()
@admin_required()
def get(codigo):
    user = User.query.filter_by(id=codigo).first()
    if user:
        user = user.__dict__
        user.pop('_sa_instance_state')
        return jsonify(user)
    else:
        return abort(400, 'Product Not Found')
    
@usuarios.route('/get/vendas/<codigo>')
@jwt.jwt_required()
@admin_required()
def get_vendas(codigo):
    usuario = User.query.filter_by(id=codigo).first()
    if usuario:
        data = usuario.vendas
        vendas = []
        for venda in data:
            venda = venda.__dict__
            venda.pop('_sa_instance_state')
            vendas.append(venda)
        return jsonify(vendas)
##########################################################################
    
#Update
@usuarios.route('/edit/<codigo>', methods=['PUT'])
@jwt.jwt_required()
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
    
#Delete
@usuarios.route('/delete/<codigo>', methods=['DELETE'])
@jwt.jwt_required()
@admin_required()
def delete(codigo):
    user = User.query.filter_by(id=codigo).first()
    if user:
        user.delete()
        db.session.commit()
        return ''
    else:
        return abort(400, "User Not Found")
##########################################################################
