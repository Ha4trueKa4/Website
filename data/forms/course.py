from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms import BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired

class CourseForm(FlaskForm):
    name = EmailField('Название курса', validators=[DataRequired()])
    description = StringField('Описание курса', validators=[DataRequired(), ])
    submit = SubmitField('Добавить')
