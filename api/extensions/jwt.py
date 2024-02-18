from flask_jwt_extended import JWTManager
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
    pass
