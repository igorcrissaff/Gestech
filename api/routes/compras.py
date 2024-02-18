#Setup
from flask import Blueprint, request, abort
import flask_jwt_extended as jwt

from ..models import db
from ..models.compra import Compra
from ..models.produto import Produto

compras = Blueprint('compras', __name__)
##########################################################################

#Create
@compras.route('/add', methods=["POST"])
@jwt.jwt_required()
def add():
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        produto = Produto.query.filter_by(id=request.json['id_produto']).first()
        if produto:
            db.session.add(Compra(request.json))
            produto.estoque += request.json['quantidade']
            db.session.commit()
            return 'OK'
        else:
            return 'Produto inexistente', 400
    else:
        return abort(401)
##########################################################################

#Read
@compras.route('/get_all', methods=['GET'])
@jwt.jwt_required()
def get_all():
    user = jwt.get_current_user()
    if user.cargo == 'admin':
        data = db.session.query(
            Compra, Produto.nome
            ).join(
                Produto, Compra.id_produto == Produto.id
                ).all()
        compras = []
        for item in data:
            compra = item[0].__dict__
            compra.pop('_sa_instance_state')
            compra['nome_produto'] = item[1]
            compras.append(compra)
        return compras
    else:
        return abort(401)

"""
@compras.route('/get_many', methods=['GET'])
def get_many():
    try:
        filtro = []
        for attr, value in request.json.items():
            filtro.append(getattr(Compra, attr) == value)
        
        data = db.session.query(
            Compra, Produto.nome
            ).join(
                Produto, compra.id_produto == Produto.id
                ).filter(*filtro).all()
        
        compras = []
        for item in data:
            compra = item[0].__dict__
            compra.pop('_sa_instance_state')
            compra['nome_produto'] = item[1]
            compras.append(compra)
        return compras
    except Exception as erro:
        return str(erro), 400
"""
##########################################################################
