from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField
from wtforms.validators import DataRequired
from app.models import ProStatus

class ScheduleForm(FlaskForm):
    pro_status = SelectField(default=1,coerce=int)
    ui_schedule = StringField()
    back_schedule = StringField()
    front_schedule = StringField()
    test_schedule = StringField()
    submit = SubmitField('提交')

    def __init__(self):
        super(ScheduleForm, self).__init__()
        self.pro_status.choices = [(pro_status.id,pro_status.name)
                                 for pro_status in ProStatus.query.order_by(ProStatus.name).all()]


