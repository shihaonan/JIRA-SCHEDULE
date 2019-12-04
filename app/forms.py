from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,HiddenField,SelectField
from wtforms.validators import DataRequired,Length
from app.models import ProStatus


class PostForm(FlaskForm):
    body = TextAreaField('内容',validators=[DataRequired()])
    body_html = TextAreaField('html内容')
    submit = SubmitField()


class CreateBigIssueForm(FlaskForm):
    jira_key = StringField('jira编号',validators=[Length(1, 20)])
    status = StringField('jira状态',validators=[Length(1, 30)])
    pro_status = SelectField('项目状态',coerce=int,default=1)
    summary = StringField('需求标题',validators=[Length(1, 255)])
    creator = StringField('创建者', validators=[Length(1, 30)])
    # related_issues =
    submit = SubmitField()

    def __init__(self):
        super(CreateBigIssueForm, self).__init__()
        self.pro_status.choices = [(pro_status.id, pro_status.name)
                                 for pro_status in ProStatus.query.order_by(ProStatus.name).all()]

    # ui_schedule = db.Column(db.String(66))
    # back_schedule = db.Column(db.String(66))
    # front_schedule = db.Column(db.String(66))
    # test_schedule = db.Column(db.String(66))
    # ui_staff = db.Column(db.String(256))
    # back_staff = db.Column(db.String(256))
    # front_staff = db.Column(db.String(256))
    # test_staff = db.Column(db.String(256))