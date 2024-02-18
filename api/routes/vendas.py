#Setup
from flask import Blueprint, request, abort
from sqlalchemy.exc import OperationalError, IntegrityError
import flask_jwt_extended as jwt

from ..models import db
from ..models.venda import Venda
from ..models.produto import Produto
from ..models.user import User

vendas = Blueprint('venda', __name__)
##########################################################################

#Create
@vendas.route('/add', methods=["POST"])
@jwt.jwt_required()
def add():
    produto = Produto.query.filter_by(id=request.json['id_produto']).first()
    if produto:
        try:
            db.session.add(Venda(request.json))
            produto.estoque -= request.json['quantidade']
            db.session.commit()
        except IntegrityError as erro:
            return str(erro), 400
        except OperationalError as erro:
            return str(erro), 400
        else:
            return 'OK'
    else:
        return 'Produto inexistente', 400
##########################################################################

#Read
@vendas.route('/get_all', methods=['GET'])
@jwt.jwt_required()
def get_all():
    data = db.session.query(
        Venda, Produto.nome, User.nome
        ).join(
            Produto, Venda.id_produto == Produto.id
            ).join(
                User, Venda.id_vendedor == User.id
                ).all()
    vendas = []
    for item in data:
        venda = item[0].__dict__
        venda.pop('_sa_instance_state')
        venda['nome_produto'] = item[1]
        venda['nome_vendedor'] = item[2]
        vendas.append(venda)
    return vendas


"""
@vendas.route('/get_many', methods=['GET'])
def get_many():
    filtro = []
    for attr, value in request.json.items():
        filtro.append(getattr(Venda, attr) == value)
    
    data = db.session.query(
        Venda, Produto.nome, User.nome
        ).join(
            Produto, Venda.id_produto == Produto.id
            ).join(
                User, Venda.id_vendedor == User.id
                ).filter(*filtro).all()
    
    vendas = []
    for item in data:
        venda = item[0].__dict__
        venda.pop('_sa_instance_state')
        venda['nome_produto'] = item[1]
        venda['nome_vendedor'] = item[2]
        vendas.append(venda)
    return vendas

@vendas.route('/get/<codigo>')
def get(codigo):
    produto = Produto.query.filter_by(id=codigo).first()
    if produto:
        data = produto.vendas
        vendas = []
        for venda in data:
            venda = venda.__dict__
            venda.pop('_sa_instance_state')
            vendas.append(venda)
        return vendas
    else:
        return 'Produto inexistente', 400
"""        
##########################################################################
