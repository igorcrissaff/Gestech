#Setup
from flask import Blueprint, request, abort
import flask_jwt_extended as jwt

from ..extensions.jwt import admin_required

from ..models import db
from ..models.compra import Compra
from ..models.produto import Produto

compras = Blueprint('compras', __name__)
##########################################################################

#Create
@compras.route('/add', methods=["POST"])
@jwt.jwt_required()
@admin_required()
def add():
    produto = Produto.query.filter_by(id=request.json['id_produto']).first()
    if produto:
        db.session.add(Compra(**request.json))
        produto.estoque += request.json['quantidade']
        db.session.commit()
        return 'OK'
    else:
        return abort(400, 'Product Not Found')
##########################################################################

#Read
@compras.route('/get_all', methods=['GET'])
@jwt.jwt_required()
@admin_required()
def get_all():
    json = request.get_json(silent=True)
    filtros = []
    if json:
        for attr, value in json.items():
            if attr == 'start_date':
                item = getattr(Compra, 'data') >= value
            elif attr == 'end_date':
                item = getattr(Compra, 'data') <= value
            else:
                item = getattr(Compra, attr) == value
            filtros.append(item)
    
    data = Compra.query.filter(*filtros).all() 
    if data:
        compras = []
        for item in data:
            compra = item.__dict__

            compra['produto'] = item.produto.dict()

            compra.pop('id_produto')
            compra.pop('_sa_instance_state')

            compras.append(compra)
        
        return compras
    else:
        return ''

@compras.route('/get/<codigo>', methods=['GET'])
@jwt.jwt_required()
@admin_required()
def get(codigo):  
    data = Compra.query.filter_by(compra=codigo).first()
    if data:
        compra = data.__dict__

        compra['produto'] = data.produto.dict()

        compra.pop('id_produto')
        compra.pop('_sa_instance_state')
        return compra
    else:
        return abort(400, 'Trade Not Found')
##########################################################################
