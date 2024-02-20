from flask import Blueprint, request
import flask_jwt_extended as jwt
from datetime import timedelta

from ..models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login/<pin>')
def login(pin):
    try:
        user = User.query.filter_by(id=pin).first()
        if not user:
            return 'Usuario inexistente', 400
        
        else:
            token = jwt.create_access_token(
                identity= user,
                expires_delta=timedelta(days=1)
                )
            return token
        
    except Exception as erro:
        return str(erro), 400
    
