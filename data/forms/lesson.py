from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import StringField, SubmitField
from data import db_session
from data.lessons import Lesson


class LessonForm(FlaskForm):
    def equal_required(form, field):
        db_sess = db_session.create_session()
        lessons = db_sess.query(Lesson)
        for lesson in lessons:
            if field.data == lesson.name:
                raise ValidationError('Совпадают названия уроков')
    name = StringField('Название урока', validators=[DataRequired(), equal_required])
    submit = SubmitField('Добавить')


class TheoryForm(FlaskForm):
    name = StringField('Название урока')
    
    submit = SubmitField('Сохранить')