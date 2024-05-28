#Setup
from flask_restful import Resource, request, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

from ..extensions.jwt import admin_required
from ..extensions.cache import cache

from ..models import db
from ..models.user import User


class Users(Resource):

    @jwt_required()
    def get(self):
        args = request.args
        filters = []
        for attr, value in args.items():
            if hasattr(User, attr):
                filters.append(getattr(User, attr) == value)

        users = User.query.filter(*filters).all()
        if users:
            users = [user.dict for user in users]
            return users
        else:
            return 'None'
    
    @admin_required()
    def post(self):
        try:
            user = User(**request.json)
            db.session.add(user)
            db.session.commit()
            return 'User Posted'
        except IntegrityError:
            return abort(400, message="User Id Already Registered")
        
    @admin_required()
    def patch(self):
        user_id = request.args.get('id')
        if not user_id:
            return abort(400, 'Missing Id')
        
        user = User.query.get(user_id)
        if not user:
            return abort(400, 'User Not Found')
        
        if 'id' in request.json.keys():
            return abort(400, message='Id Cannot Be Changed')

        for attr, value in request.json.items():
            if hasattr(user, attr) and attr != 'id':
                setattr(user, attr, value)
        db.session.commit()
        return 'User Patched'
    
    @admin_required()  
    def remove():
        user_id = request.args.get('id')
        if not user_id:
            return abort(400, message='Missing Id')

        user = User.query.get(user_id)
        if not user:
            return abort(400, "User Not Found")

        db.session.delete(user)
        db.session.commit()
        return ''
        