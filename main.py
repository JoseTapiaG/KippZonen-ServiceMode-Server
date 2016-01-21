import math
from datetime import datetime

import flask
from flask import Flask, request, render_template, make_response
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from forms import LoginForm, validate_user, CreateUserForm, ProfileForm
from messages import update_error
from models import db, Registro, User, Perfil

from automatizacion import SchedulerManager

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = CreateUserForm(request.form)
    if request.method == "POST":
        if form.validate():
            try:
                user = User(email=form.email.data, user=form.user.data, password=form.password.data)
                db.session.add(user)
                db.session.commit()
                return flask.redirect("login")
            except Exception:
                db.session.rollback()
                return render_template("create_user.html", form=form, error="Hubo un error en DB")
    return render_template("create_user.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    next = flask.request.args.get('next')
    form = LoginForm(request.form)
    if form.validate():
        user = validate_user(form.user._value(), form.password._value())
        if user:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return flask.redirect(next or "filter")
    return render_template("login.html", form=form, next=next)


@app.route("/logout", methods=["GET"])
@login_required
def logout_page():
    """Logout the current user."""
    logout()
    return render_template("logout.html")


def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()


@app.route("/index")
@login_required
def index():
    return render_template('index.html', login_form=LoginForm())


@app.route("/getAll")
def get_all():
    registros = Registro.query.all()
    return render_template('registers.html', registros=registros)


@app.route("/filter")
@login_required
def filter_registers():
    return render_template('filter.html')


@app.route("/getRegistersForDate")
def get_registers_for_date():
    date_ini = datetime.strptime(request.args.get("dateIni"), "%Y-%m-%d")
    date_end = datetime.strptime(request.args.get("dateEnd"), "%Y-%m-%d")
    page = int(request.args.get("page"))
    registros = Registro.query.filter(Registro.fecha.between(date_ini, date_end)).offset((page - 1) * 10).limit(10)
    total = Registro.query.count()
    return render_template('registers.html', registros=registros, date_ini=date_ini.strftime("%Y-%m-%d"),
                           date_end=date_end.strftime("%Y-%m-%d"), total_pages=math.ceil(total / 10.0))


@app.route("/csv")
def export_csv():
    date_ini = datetime.strptime(request.args.get("dateIni"), "%Y-%m-%d")
    date_end = datetime.strptime(request.args.get("dateEnd"), "%Y-%m-%d")
    registros = Registro.query.filter(Registro.fecha.between(date_ini, date_end))
    csv_str = ""
    for registro in registros:
        csv_str += registro.fecha.strftime("%Y-%m-%d") + "," + str(registro.dato1) + "," + str(
                registro.dato2) + "," + str(registro.dato3) + "\n"
    output = make_response(csv_str)
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route("/save", methods=['POST'])
def save():
    try:
        registro = Registro(
                fecha=datetime.strptime(request.form['fecha'], "%Y-%m-%d %H:%M:%S"),
                dato1=request.form['dato1'],
                dato2=request.form['dato2'],
                dato3=request.form['dato3']
        )
        db.session.add(registro)
        db.session.commit()
    except Exception:
        db.session.rollback()
    return "Ok"


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user

    if request.method == "GET":
        form = ProfileForm()
        form.set_values(user)

    if request.method == "POST":
        form = ProfileForm(request.form)
        form.id = user.id
        if form.validate():
            try:
                user.user = form.user.data
                user.email = form.email.data
                if form.password.data:
                    user.set_password(form.password.data)
                user.perfil.periodicidad = form.periodicity.data
                db.session.add(user)
                db.session.commit()
                app.scheduler_manager.add_job(user.perfil)
                logout()
                return flask.redirect("login")
            except Exception as e:
                db.session.rollback()
                error = update_error
                return render_template("profile.html", form=form, error=error)
    return render_template('profile.html', form=form)


def create_db():
    try:
        db.create_all()
    except Exception as e:
        db.session.rollback()
    return "ok"


def populate_db():
    try:
        registro = Registro(datetime.now(), 0.051, 0.072, 0.093)
        user = User("jose.wt@gmail.com", "jose", "pass")
        user.perfil = Perfil()
        db.session.add(registro)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return "Ok"


@app.before_first_request
def initialize():
    create_db()
    populate_db()
    print("Partimos")
    app.scheduler_manager = SchedulerManager(Perfil.query.all())
    app.scheduler_manager.start()


if __name__ == "__main__":
    app.config["SECRET_KEY"] = "ITSASECRET"
    app.run(port=5000, debug=True)
