#Setup
from flask import Blueprint, request, abort, jsonify
import flask_jwt_extended as jwt

from ..models import db
from ..models.user import User

usuarios = Blueprint('usuarios', __name__)
##########################################################################

#Create
@usuarios.route('/add', methods=["POST"])
@jwt.jwt_required()
def add():
    user = jwt.get_current_user()
    if user.cargo == 'admin':  
        db.session.add(User(request.json))
        db.session.commit()
        return ""
    else:
        return abort(401, 'Admin Required')
##########################################################################

#Read
@usuarios.route('/get_all', methods=['GET'])
@jwt.jwt_required()
def get_all():
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        data = User.query.all()
        users = []
        for user in data:
            user = user.__dict__
            user.pop('_sa_instance_state')
            users.append(user)
        return jsonify(users)
    else:
        return abort(401, 'Admin Required')
    
@usuarios.route('/get/<codigo>', methods=['GET'])
@jwt.jwt_required()
def get(codigo):
    user = jwt.get_current_user()
    if user.id == codigo or user.cargo == 'admin':
        user = User.query.filter_by(id=codigo).first()
        if user:
            user = user.__dict__
            user.pop('_sa_instance_state')
            return user
        else:
            return abort(401, 'Product Not Found')
    else:
        return abort(401)
    
@usuarios.route('/get/vendas/<codigo>')
@jwt.jwt_required()
def get_vendas(codigo):
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        usuario = User.query.filter_by(id=codigo).first()
        if usuario:
            data = usuario.vendas
            vendas = []
            for venda in data:
                venda = venda.__dict__
                venda.pop('_sa_instance_state')
                vendas.append(venda)
            return vendas
        else:
            return abort(400, 'User Not Found')
##########################################################################
    
#Update
@usuarios.route('/edit/<codigo>', methods=['PUT'])
@jwt.jwt_required()
def edit(codigo):
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        usuario = User.query.filter_by(id=codigo).first()
        if usuario:
            for key, value in request.json.items():
                setattr(usuario, key, value)
            db.session.commit()
            return jsonify('OK', 200)
        else:
            return abort(401, 'Product Not Found')
    else:
        return abort(401)
##########################################################################
    
#Delete
@usuarios.route('/delete/<codigo>', methods=['DELETE'])
@jwt.jwt_required
def delete(codigo):
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        User.query.filter_by(id=codigo).delete()
        db.session.commit()
        return ''
    else:
        return abort(401)
##########################################################################
