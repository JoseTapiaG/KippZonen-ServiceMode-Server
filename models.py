from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db_session = SQLAlchemy(app)


class Registro(db_session.Model):
    id = db_session.Column(db_session.Integer, primary_key=True)
    fecha = db_session.Column(db_session.DateTime, unique=True)
    dato1 = db_session.Column(db_session.Float)
    dato2 = db_session.Column(db_session.Float)
    dato3 = db_session.Column(db_session.Float)

    def __init__(self, fecha, dato1, dato2, dato3):
        self.fecha = fecha
        self.dato1 = dato1
        self.dato2 = dato2
        self.dato3 = dato3
