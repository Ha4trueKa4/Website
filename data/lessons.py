import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Lesson(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    theory = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    theory_title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    completed_by_users = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_in_course = sqlalchemy.Column(sqlalchemy.Integer)
    course_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("cources.id"))

    tasks = orm.relationship("Task", back_populates='lesson')
    course = orm.relationship("Course")