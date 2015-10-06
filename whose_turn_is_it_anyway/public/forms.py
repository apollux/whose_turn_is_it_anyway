# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired

from whose_turn_is_it_anyway.user.models import User


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user or not self.user.check_password(self.password.data):
            self.username.errors.append('Invalid username and password combination')
            return False

        if not self.user.active:
            self.username.errors.append('User not activated')
            return False
        return True
