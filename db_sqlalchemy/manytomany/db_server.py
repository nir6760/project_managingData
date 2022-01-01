
from flask import Flask

from db_sqlalchemy.common.base import connDBParams
from sqlalchemy import Column, String, Table, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship


# singeltone class for connDB
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class myApp(metaclass=Singleton):
    def __init__(self):
        self.MY_TOKEN = "5062861976:AAFl2UAliIU4I5a4JS16SU6X82dOdHcD7cU"
        self.app = Flask(__name__)
        self.connDBParams_obj = connDBParams(app=self.app)

        class User(self.connDBParams_obj.db.Model):
            __tablename__ = 'users'

            id_user = Column(String, primary_key=True)
            user_name = Column(String, nullable=False)

            def __init__(self, id_user, user_name):
                self.id_user = id_user
                self.user_name = user_name

        self.User_class = User
        Base = self.connDBParams_obj.db

        users_questions_table = Table(
            'users_questions', Base.metadata,
            Column('id_user', String, ForeignKey('users.id_user', onupdate="CASCADE", ondelete="CASCADE")),

            Column('id_poll', String),
            Column('id_question', String),

            Column('id_answer', String),
            ForeignKeyConstraint(('id_poll', 'id_question'),
                                 ['polls.id_poll', 'polls.id_question'], onupdate="CASCADE", ondelete="CASCADE")
        )

        admins_polls_table = Table(
            'admins_polls', Base.metadata,
            Column('id_admin', String, ForeignKey('admins.id_admin', onupdate="CASCADE", ondelete="CASCADE")),

            Column('id_poll', String),
            Column('id_question', String),

            ForeignKeyConstraint(('id_poll', 'id_question'),
                                 ['polls.id_poll', 'polls.id_question'], onupdate="CASCADE", ondelete="CASCADE"),
        )

        class Poll(self.connDBParams_obj.db.Model):
            __tablename__ = 'polls'

            id_poll = Column(String, primary_key=True)
            id_question = Column(String, primary_key=True)

            users_questions_rel = relationship("User", secondary=users_questions_table)
            admins_polls_rel = relationship("Admin", secondary=admins_polls_table)

            def __init__(self, id_poll, id_question):
                self.id_poll = id_poll
                self.id_question = id_question

        self.Poll_class = Poll

        class Admin(self.connDBParams_obj.db.Model):
            __tablename__ = 'admins'

            id_admin = Column(String, primary_key=True)
            admin_name = Column(String, nullable=False)
            hash_password = Column(String, nullable=False)

            def __init__(self, id_admin, admin_name, hash_password):
                self.id_admin = id_admin
                self.admin_name = admin_name
                self.hash_password = hash_password

        self.Admin_class = Admin




