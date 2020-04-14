import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Jobs(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    end_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)

    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relation('User', back_populates='jobs')
