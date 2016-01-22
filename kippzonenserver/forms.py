import messages
import my_validators
from enums import Periodicidad
from models import User
from wtforms import Form, StringField, validators, SelectField


class LoginForm(Form):
    user = StringField(u'user', validators=[validators.input_required(messages.required)])
    password = StringField(u'password', validators=[validators.input_required(messages.required)])


def validate_user(user_name, password):
    if user_name is not None:
        user = User.query.filter_by(user=user_name).first()
    else:
        user = User.query.filter_by(email=user_name).first()

    if not user:
        return None

    if user.check_password(password):
        return user
    else:
        return None


class CreateUserForm(Form):
    user = StringField(u'user', validators=[validators.input_required(messages.required), my_validators.user_exists()])
    email = StringField(u'email',
                        validators=[validators.input_required(messages.required), my_validators.mail_exists()])
    password = StringField(u'password', validators=[validators.input_required(messages.required),
                                                    validators.equal_to('confirm_password',
                                                                        message='Passwords deben ser iguales')])
    confirm_password = StringField(u'confirm_password', validators=[validators.input_required(messages.required)])


class ProfileForm(Form):
    user = StringField(u'user', validators=[validators.input_required(messages.required),
                                            my_validators.user_exists(new_user=False)])
    email = StringField(u'email', validators=[validators.input_required(messages.required),
                                              my_validators.mail_exists(new_user=False)])
    password = StringField(u'password', validators=[validators.equal_to('confirm_password',
                                                                        message='Passwords deben ser iguales')])
    confirm_password = StringField(u'confirm_password')
    periodicity = SelectField(u'periodicity', choices=[
        (Periodicidad.diaria.value, Periodicidad.diaria.value),
        (Periodicidad.semanal.value, Periodicidad.semanal.value),
        (Periodicidad.mensual.value, Periodicidad.mensual.value)])

    def set_values(self, user):
        self.user.data = user.user
        self.email.data = user.email
        self.periodicity.data = user.perfil.periodicidad
