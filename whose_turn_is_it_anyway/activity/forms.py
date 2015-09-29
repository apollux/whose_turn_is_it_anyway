# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, FieldList, BooleanField
from wtforms.validators import DataRequired, Length

from .models import Activity

class CreateActivityForm(Form):
    name = StringField('Activity',
                       validators=[DataRequired(), Length(min=3, max=25)])
    current_user_as_participant = BooleanField('Include me as participant')
    participants = FieldList(StringField('Name', validators=[DataRequired()]))

    def __init__(self, *args, **kwargs):
        super(CreateActivityForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(CreateActivityForm, self).validate()
        if not initial_validation:
            return False
        return True
