from functools import wraps

from flask import abort, current_app
from flask_jwt_extended import JWTManager, get_current_user, jwt_required
from ..models.user import User

jwt_manager = JWTManager()

@jwt_manager.user_identity_loader
def load_identity(user):
    return user.id

@jwt_manager.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            user = get_current_user()
            if user.id in current_app.config['ADMINS']:
                return fn(*args, **kwargs)
            else:
                return abort(403, 'Admin Required')

        return decorator

    return wrapper
