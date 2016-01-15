from datetime import datetime

from flask import Flask, request, render_template, make_response

import database
import math
from models import db_session, Registro

app = Flask(__name__)
app.debug = True


@app.route("/createAll")
def create_all():
    db_session = database.get_db()
    db_session.create_all()
    registro = Registro(datetime.now(), 0.051, 0.072, 0.093)
    db_session.session.add(registro)
    db_session.session.commit()
    return "ok"


@app.route("/getAll")
def get_all():
    registros = Registro.query.all()
    return render_template('registers.html', registros=registros)


@app.route("/filter")
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
    date_ini = datetime.strptime(request.args.get("date_ini"), "%Y-%m-%d")
    date_end = datetime.strptime(request.args.get("date_end"), "%Y-%m-%d")
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
        db_session = database.get_db()
        db_session.session.add(registro)
        db_session.session.commit()
    except 'Exception':
        db_session.session.rollback()
    return "Ok"


if __name__ == "__main__":
    app.run()
