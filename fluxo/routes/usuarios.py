#Setup
from flask import Blueprint, request, abort, jsonify
import flask_jwt_extended as jwt

from ..extensions.jwt import admin_required
from ..extensions.cache import cache

from ..models import db
from ..models.user import User

usuarios = Blueprint('usuarios', __name__)
##########################################################################

# Read
@usuarios.route('', methods=['GET'])
@admin_required()
def get():
    args = request.args
    filters = []
    for attr, value in args.items():
        if hasattr(User, attr) and attr in ['id', 'name', 'email', 'phone']:
            filters.append(getattr(User, attr) == value)

    users = User.query.filter(*filters).all()
    if users:
        users = [user.dict for user in users]
        return users
    else:
        return 'None'

# Create
@usuarios.route('', methods=["POST"])
@admin_required()
def add():
    try:
        user = User(**request.json)
        db.session.add(user)
        db.session.commit()
        return '',201
    except Exception as erro:
        return abort(400, repr(erro))
##########################################################################
    
# Update
@usuarios.route('', methods=['PATCH'])
@admin_required()
def edit():
    user_id = request.args.get('id')
    user = User.query.get(user_id)
    if user:
        for attr, value in request.json.items():
            if hasattr(user, attr) and attr != 'id':
                setattr(user, attr, value)
        db.session.commit()
        return '', 204
    else:
        return abort(400, 'User Not Found')
##########################################################################
    
# Delete
@usuarios.route('', methods=['DELETE'])
@admin_required()
def remove():
    user_id = request.args.get('id')
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return '', 200
    else:
        return abort(400, "User Not Found")
##########################################################################
