from flask import Flask

from .models import *

from .routes.auth import auth
from .routes.estoque import estoque
from .routes.usuarios import usuarios
from .routes.vendas import vendas
from .routes.compras import compras

#from .extensions.cache import cache
from .extensions.jwt import jwt_manager

App = Flask(__name__, instance_relative_config=True)

App.register_blueprint(auth, url_prefix='/auth')

App.register_blueprint(estoque, url_prefix='/estoque')
App.register_blueprint(usuarios, url_prefix='/usuarios')
App.register_blueprint(vendas, url_prefix='/vendas')
App.register_blueprint(compras, url_prefix='/compras')

App.config.from_pyfile('BaseConfig.py')
App.config.from_pyfile('DevelopmentConfig.py')

#cache.init_app(App)
jwt_manager.init_app(App)
db.init_app(App)


@App.route('/create_all')
def create_all():
    db.create_all()
    return 'ok'

    