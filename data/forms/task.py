from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms import BooleanField, SubmitField, RadioField, StringField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    submit = SubmitField('ответить')