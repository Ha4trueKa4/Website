from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms import BooleanField, SubmitField, RadioField, StringField, TextAreaField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    submit = SubmitField('ответить')


class UpdateTaskForm(FlaskForm):
    name_task = StringField('Название задания', validators=[DataRequired()])
    text_task = TextAreaField('Текст задания')

    text_task1 = StringField('Вариант 1', validators=[DataRequired()])
    radio_task1 = RadioField('Правильный вариант', choices=['1', '2', '3', '4'])

    text_task2 = StringField('Вариант 2', validators=[DataRequired()])

    text_task3 = StringField('Вариант 3', validators=[DataRequired()])

    text_task4 = StringField('Вариант 4', validators=[DataRequired()])

    submit = SubmitField('Сохранить')

