from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import json

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)


class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False)
    password = db.Column(db.String(200), unique=False)
    surname = db.Column(db.String(50), unique=False)
    last_name = db.Column(db.String(50), unique=False)
    contact = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(50), unique=True)
    country = db.Column(db.String(50), unique=False)
    city = db.Column(db.String(50), unique=False)
    adress = db.Column(db.String(100), unique=False)
    zipcode = db.Column(db.String(50), unique=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Zákazník ('{self.id}', uživatelské jméno: '{self.username}', jméno a příjmení: '{self.surname}' '{self.last_name}', email: '{self.email}')"



class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return "{}"
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default="Čeká na zpracování", nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEncodedDict)

    def __repr__(self):
        return f"Objednávka (ID: '{self.id}', Číslo objednávky: '{self.invoice}', Status: '{self.status}', Zákazník ID: '{self.customer_id}', Den vytvoření: '{self.date_created}')"




db.create_all()

