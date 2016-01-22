from kippzonenserver import app
from flask_mail import Mail, Message

mail = Mail()

app.config.update(dict(
        DEBUG=True,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME='adkmovil@niclabs.cl',
        MAIL_PASSWORD='xxxxxxx',
))
mail.init_app(app)


def send_csv(title, data, receiver):
    msg = Message(title,
                  sender="adkmovil@niclabs.cl",
                  recipients=[receiver])
    msg.attach("test.csv", "text/csv", data)
    mail.send(message=msg)
