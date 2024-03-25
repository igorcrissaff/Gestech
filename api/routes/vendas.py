#Setup
from flask import Blueprint, request, abort
from sqlalchemy.exc import OperationalError, IntegrityError
import flask_jwt_extended as jwt

from ..extensions.jwt import admin_required

from ..models import db
from ..models.sale import Venda
from ..models.produto import Produto

vendas = Blueprint('venda', __name__)
##########################################################################

#Create
@vendas.route('/add', methods=["POST"])
@jwt.jwt_required()
def add():
    produto = Produto.query.filter_by(id=request.json['id_produto']).first()
    if produto:
        db.session.add(Venda(**request.json))
        produto.estoque -= request.json['quantidade']
        db.session.commit()    
        return 'OK'
    else:
        return 'Produto inexistente', 400
##########################################################################

#Read
@vendas.route('/get_all', methods=['GET'])
@jwt.jwt_required()
@admin_required()
def get_all():
    json = request.get_json(silent=True)
    filtros = []
    if json:
        filtros = [getattr(Venda, attr) == value for attr, value in json.items()]

    data = Venda.query.filter(*filtros).all()

    vendas = []
    if data:
        for item in data:
            venda = item.__dict__

            venda['produto'] = {
                "id": item.produto.id, 
                "nome": item.produto.nome, 
                "valor": item.produto.valor
                }
            venda['vendedor'] = {
                "id": item.vendedor.id, 
                "nome": item.vendedor.nome
                }

            venda.pop('id_produto')
            venda.pop('id_vendedor')

            venda.pop('_sa_instance_state')
            vendas.append(venda)
        return vendas

@vendas.route('/get/<codigo>', methods=['GET'])
@jwt.jwt_required()
@admin_required()
def get(codigo):  
    data = Venda.query.filter_by(venda=codigo).first()
    venda = None
    if data:
        venda = data.__dict__

        venda['produto'] = {
            "id": data.produto.id, 
            "nome": data.produto.nome, 
            "valor": data.produto.valor
            }
        venda['vendedor'] = {
            "id": data.vendedor.id, 
            "nome": data.vendedor.nome
            }

        venda.pop('id_produto')
        venda.pop('id_vendedor')
        venda.pop('_sa_instance_state')
        return venda
    else:
        return abort(400, 'Trade Not Found')
     
##########################################################################
