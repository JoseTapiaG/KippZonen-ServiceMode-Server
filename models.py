from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, unique=True)
    dato1 = db.Column(db.Float)
    dato2 = db.Column(db.Float)
    dato3 = db.Column(db.Float)

    def __init__(self, fecha, dato1, dato2, dato3):
        self.fecha = fecha
        self.dato1 = dato1
        self.dato2 = dato2
        self.dato3 = dato3





