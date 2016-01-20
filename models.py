from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from enums import Periodicidad

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


class User(db.Model):
    email = db.Column(db.String, primary_key=True)
    user = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    perfil = db.relationship("Perfil", uselist=False, back_populates="user")

    def __init__(self, email, user, password):
        self.email = email
        self.user = user
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String,db.ForeignKey('user.email'))
    user = db.relationship("User", back_populates="perfil")
    periodicidad = db.Column(db.Enum(Periodicidad.diaria.value, Periodicidad.semanal.value, Periodicidad.mensual.value),
                             default="diaria")
