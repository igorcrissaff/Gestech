from flask_restful import Api
from . import auth, users, products, sales, purchases 

api = Api()

api.add_resource(auth.Auth, '/auth')
api.add_resource(users.Users, '/users')
api.add_resource(products.Products, '/products')
api.add_resource(sales.Sales, '/sales')
api.add_resource(purchases.Purchases, '/purchases')
