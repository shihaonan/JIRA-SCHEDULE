from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,HiddenField
from wtforms.validators import DataRequired,Length


class PostForm(FlaskForm):
    body = TextAreaField('内容',validators=[DataRequired()])
    body_html = TextAreaField('html内容')
    submit = SubmitField()