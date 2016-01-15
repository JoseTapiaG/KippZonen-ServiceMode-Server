from flask import Flask, request, render_template, make_response
from models import db, Registro
from datetime import datetime
import database, math

app = Flask(__name__)
app.debug = True


@app.route("/SaveData")
def hello():
    db = database.get_db()
    for user in db.execute('select * from Persona'):
        print user[0], 'has the id', user[1]
    database.close_connection()
    return "Hello World!"


@app.route("/createAll")
def createAll():
    db.create_all()
    registro = Registro(datetime.now(), 0.051, 0.072, 0.093)
    db.session.add(registro)
    db.session.commit()
    return "ok"


@app.route("/getAll")
def getAll():
    registros = Registro.query.all()
    return render_template('registers.html', registros=registros)


@app.route("/filter")
def filter():
    return render_template('filter.html')


@app.route("/getRegistersForDate")
def getRegistersForDate():
    dateIni = datetime.strptime(request.args.get("dateIni"), "%Y-%m-%d")
    dateEnd = datetime.strptime(request.args.get("dateEnd"), "%Y-%m-%d")
    page = int(request.args.get("page"))
    registros = Registro.query.filter(Registro.fecha.between(dateIni, dateEnd)).offset((page - 1) * 10).limit(10)
    total = Registro.query.count()
    return render_template('registers.html', registros=registros, dateIni=dateIni.strftime("%Y-%m-%d"),
                           dateEnd=dateEnd.strftime("%Y-%m-%d"), totalPages=math.ceil(total / 10.0))


@app.route("/csv")
def exportCSV():
    dateIni = datetime.strptime(request.args.get("dateIni"), "%Y-%m-%d")
    dateEnd = datetime.strptime(request.args.get("dateEnd"), "%Y-%m-%d")
    registros = Registro.query.filter(Registro.fecha.between(dateIni, dateEnd))
    csvStr = ""
    for registro in registros:
        csvStr += registro.fecha.strftime("%Y-%m-%d") + "," + str(registro.dato1) + "," + str(
            registro.dato2) + "," + str(registro.dato3) + "\n"
    output = make_response(csvStr)
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
    except:
        db.session.rollback()
    return "Ok"


if __name__ == "__main__":
    app.run()
