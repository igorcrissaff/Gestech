from . import db

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.String(13), nullable=False, primary_key=True)
    nome = db.Column(db.String(50) , nullable=False, unique=True)
    valor = db.Column(db.Float(), nullable=False)
    unidade = db.Column(db.Enum('Un', 'Kg', 'Lt'), nullable=False)
    estoque = db.Column(db.Float(), nullable=False, default=0)

    vendas = db.relationship('Venda', backref='produto')
    compras = db.relationship('Compra', backref='produto')

    def __init__(self, id, nome, valor, unidade):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.unidade = unidade

    def get_dict(self, id):
        produto = self.query.filter_by(id=id).first()
        if produto:
            produto = produto.__dict__
            produto.pop('_sa_instance_state')
            return produto