from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from re import match
from datetime import date

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(4), nullable=False, primary_key=True)
    username = db.Column(db.String(50) , nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.string(100), nullable=False)
    phone = db.Column(db.String(13))
    birth_date = db.Column(db.Date(), nullable=False)

    sales = db.relationship('sale', backref='seller')

    def __init__(self, id, username, email, password, phone, birth_date):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.birth_date = birth_date
    
    def dict(self):
        user = self.__dict__
        user.pop('_sa_instance_state')
        return user

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        pass

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        pass

    @property
    def email(self):
        return self.email
    
    @email.setter
    def email(self, email):
          pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
          if match(pattern, email):
              self._email = email

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, password: str):
        self._password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self._password, password)
    
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, phone: str):
        if phone.isnumeric() and len(phone) <= 13:
            self._phone = phone
        else:
            raise ValueError

    @property
    def birth_date(self):
        return self._birth_date
    
    @birth_date.setter
    def birth_date(self, birth_date):
        today = date.today()
        if birth_date < today:
            self._birth_date = birth_date
        else:
            raise ValueError('birth date must be prior to today date')
