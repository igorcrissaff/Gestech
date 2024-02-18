from . import db

class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.String(4), nullable=False, primary_key=True)
    nome = db.Column(db.String(50) , nullable=False, unique=True)
    cargo = db.Column(db.Enum('admin', 'caixa'), nullable=False, default='caixa')

    vendas = db.relationship('Venda', backref='vendedor')

    def __init__(self, data):
        self.id = '0'*(4-len(data['id'])) + data['id']
        self.nome = data['nome']
        self.cargo = data['cargo']
    
    def get(self, id):
        user = self.query.filter_by(id=id).first()
        return user
    
    def get_all(self):
        users = User.query.all()
        return users
