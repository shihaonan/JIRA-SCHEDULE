from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DateField
from wtforms.validators import DataRequired

class ScheduleForm(FlaskForm):
    ui_schedule = StringField()
    back_schedule = StringField()
    front_schedule = StringField()
    test_schedule = StringField()
    submit = SubmitField('提交')