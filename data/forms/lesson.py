from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import StringField, SubmitField, TextAreaField
from data import db_session
from data.lessons import Lesson
from data.tasks import Task


class LessonForm(FlaskForm):
    def equal_required(form, field):
        db_sess = db_session.create_session()
        lessons = db_sess.query(Lesson).all()
        for lesson in lessons:
            if field.data == lesson.name:
                raise ValidationError('Совпадают названия уроков')
    name = StringField('Название урока', validators=[DataRequired(), equal_required])
    submit = SubmitField('Добавить')


class CreateTaskForm(FlaskForm):
    def equal_required(form, field):
        db_sess = db_session.create_session()
        tasks = db_sess.query(Task).all()
        for task in tasks:
            if field.data == task.name:
                raise ValidationError('Совпадают названия заданий')

    name = StringField('Название урока', validators=[DataRequired(), equal_required])
    submit = SubmitField('Добавить')



class TheoryForm(FlaskForm):
    name = StringField('Название урока', validators=[DataRequired()])
    theory_title = StringField('Название теории', validators=[DataRequired()])
    theory = TextAreaField('Теория', validators=[DataRequired()])
    submit = SubmitField('Сохранить')