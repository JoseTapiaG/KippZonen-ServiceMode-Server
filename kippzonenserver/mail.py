from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

mail = Mail()
mail.init_app(app)


def send_csv(data):
    msg = Message("Hello",
                  sender="jose@niclabs.cl",
                  recipients=["jose@niclabs.cl"])

    msg.body = ""

    msg.attach("test.png", "text/csv", data)


    mail.send(message=msg)
