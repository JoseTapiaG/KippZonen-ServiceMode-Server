from kippzonenserver.models import User
from wtforms import ValidationError


def user_exists(new_user=True):
    message = 'El usuario ya existe'

    def _user_exists_new_user(form, field):
        user_by_user = User.query.filter_by(user=field.data).first()

        if user_by_user:
            raise ValidationError(message)

    def _user_exists_update_user(form, field):
        user_by_id = User.query.get(form.id)
        user_by_user = User.query.filter_by(user=field.data).first()

        if not user_by_user:
            return

        if user_by_id != user_by_user:
            raise ValidationError(message)

    if new_user:
        return _user_exists_new_user
    else:
        return _user_exists_update_user


def mail_exists(new_user=True):
    message = 'El mail ya existe'

    def _mail_exists_new_user(form, field):
        user_by_mail = User.query.filter_by(email=field.data).first()

        if user_by_mail:
            raise ValidationError(message)

    def _mail_exists_update_user(form, field):
        user_by_id = User.query.get(form.id)
        user_by_mail = User.query.filter_by(email=field.data).first()

        if not user_by_mail:
            return

        if user_by_id != user_by_mail:
            raise ValidationError(message)

    if new_user:
        return _mail_exists_new_user
    else:
        return _mail_exists_update_user
