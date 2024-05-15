from flask import Flask
from flask_restful import Api as api

from .models import db

from .resources import auth, human_resources, sales, stock

#from .extensions.cache import cache
from .extensions.jwt import jwt_manager

App = Flask(__name__, instance_relative_config=True)
Api = api(App)


Api.add_resource(auth.Auth, '/auth')
Api.add_resource(human_resources.HR, '/users')
Api.add_resource(stock.Stock, '/stock')
Api.add_resource(sales.Sales, '/sales')


App.config.from_pyfile('BaseConfig.py')
App.config.from_pyfile('DevelopmentConfig.py')

#cache.init_app(App)
jwt_manager.init_app(App)
db.init_app(App)


if __name__ == '__main__':
    App.run()
    