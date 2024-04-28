import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    correct_option = sqlalchemy.Column(sqlalchemy.String, default='')
    options = sqlalchemy.Column(sqlalchemy.String, default='')
    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lessons.id"))
    users_passed = sqlalchemy.Column(sqlalchemy.String, default='')
    id_in_lesson = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


    lesson = orm.relationship("Lesson")