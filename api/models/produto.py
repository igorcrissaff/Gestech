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

    def __init__(self, data):
        self.id = data["id"]
        self.nome = data["nome"]
        self.valor = data["valor"]
        self.unidade = data['unidade']
