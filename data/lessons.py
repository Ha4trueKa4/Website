import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class TextLesson(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'text_lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    lesson_text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    course_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("cources.id"))

    course = orm.relationship("Course")