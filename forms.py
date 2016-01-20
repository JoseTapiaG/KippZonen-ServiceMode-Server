from wtforms import Form, StringField, validators

from models import User
import messages


class LoginForm(Form):
    user = StringField(u'user', validators=[validators.input_required(messages.required)])
    password = StringField(u'password', validators=[validators.input_required(messages.required)])


def validate_user(user_name, password):
    if user_name is not None:
        user = User.query.filter_by(user=user_name).first()
    else:
        user = User.query.filter_by(email=user_name).first()

    if user.check_password(password):
        return user
    else:
        return None


class CreateUserForm(Form):
    user = StringField(u'user', validators=[validators.input_required(messages.required)])
    email = StringField(u'email', validators=[validators.input_required(messages.required)])
    password = StringField(u'password', validators=[validators.input_required(messages.required)])

    def user_exist(self):
        return User.query.get(self.email.data) is not None
