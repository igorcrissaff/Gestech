from flask import Flask

#from .extensions.cache import cache
from .extensions.jwt import jwt_manager
from .models import *
from .resources import api

app = Flask(__name__, instance_relative_config=True)


app.config.from_pyfile('BaseConfig.py')
app.config.from_pyfile('ProductionConfig.py')

#cache.init_app(App)
jwt_manager.init_app(app)
db.init_app(app)
api.init_app(app)

@app.route('/create_all')
def create_all():
    db.create_all()
    return 'ok'


if __name__ == '__main__':
    app.run()
    