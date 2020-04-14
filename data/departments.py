import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Departments(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    members = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
