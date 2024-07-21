from . import db
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import re


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(11), nullable=False, primary_key=True)
    name = db.Column(db.String(50) , nullable=False, unique=True)
    _email = db.Column(db.String(100), nullable=False, unique=True)
    _password = db.Column(db.String(265), nullable=False)
    _phone = db.Column(db.String(13))
    _birth_date = db.Column(db.Date())

    #sales = db.relationship('Sale', backref='seller')

    def __init__(self, id, name, email, password, phone, birth_date):
        self.id = id
        self.name = name
        self._email = email
        self._password = generate_password_hash(password)
        self._phone = phone
        
        birth_date = ' '.join(birth_date.split()[:4])
        self._birth_date = parse(birth_date)
        #self.birth_date = birth_date

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, email={self.email}, phone={self.phone}, birth_date={self.birth_date})>"
    
    @hybrid_property
    def dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'birth_date': self.birth_date.strftime("%d-%m-%Y")
        }
    
    # email
    @hybrid_property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        if re.fullmatch(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", email):
            self._email = email
        else:
            raise ValueError("Invalid email format")
    
    ######################
        
    # password
    @hybrid_property
    def password(self):
        return "****"
    
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self._password, password)
    ######################

    # phone
    @hybrid_property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, phone: str):
        if phone.isnumeric() and len(phone) == 13:
            self._phone = phone
        else:
            raise ValueError('invalid phone number')
    ######################
        
    #birth_date
    @hybrid_property
    def birth_date(self):
        return self._birth_date
    
    @birth_date.setter
    def birth_date(self, birth_date):
        today = date.today()
        if birth_date > today or relativedelta(date.today(), self.birth_date).years > 100:
            raise ValueError('invalid birth date')
    
    @hybrid_property
    def age(self):
        return relativedelta(date.today(), self.birth_date).years
    
