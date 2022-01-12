import uuid

from flask import Flask
import datetime

from configuration.config import bot_key
from db_sqlalchemy.common.base import connDBParams
from sqlalchemy import Column, String, INT, Table, ForeignKey, ForeignKeyConstraint, DATE, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# singeltone class for connDB
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class myApp(metaclass=Singleton):
    def __init__(self):
        self.MY_TOKEN = bot_key
        self.app = Flask(__name__)
        self.connDBParams_obj = connDBParams(app=self.app)

        class User(self.connDBParams_obj.db.Model):
            __tablename__ = 'users'

            id_user = Column(String, primary_key=True)
            user_name = Column(String, nullable=False)
            user_useranswer_rel = relationship('UserAnswer', backref='User')  # one to many

            def __init__(self, id_user, user_name):
                self.id_user = id_user
                self.user_name = user_name

        self.User_class = User
        Base = self.connDBParams_obj.db

        # generates unique ids
        def generate_uuid():
            return str(uuid.uuid4())

        class Poll(self.connDBParams_obj.db.Model):
            __tablename__ = 'polls'

            id_poll = Column(String, name="id_poll", primary_key=True)
            poll_content = Column(String)
            date = Column(DATE)
            poll_choice_rel = relationship('Choice', backref='Poll') # one to many
            poll_adminpoll_rel = relationship('AdminPoll', backref='Poll')  # one to many
            poll_polltelegram_rel = relationship('PollTelegram', backref='Poll')  # one to many

            def __init__(self, poll_content):
                #self.id_poll = generate_uuid()
                self.poll_content = poll_content
                self.date = datetime.date.today()

        self.Poll_class = Poll

        class Admin(self.connDBParams_obj.db.Model, UserMixin):
            __tablename__ = 'admins'
            admin_name = Column(String, nullable=False, primary_key=True)
            password = Column(String, nullable=False)
            token = Column(String, name="token",nullable=False , unique=True, default=generate_uuid())
            admin_adminpoll_rel = relationship('AdminPoll', backref='Admin')  # one to many

            def __init__(self,admin_name , password):
                self.admin_name = admin_name
                self.password = generate_password_hash(password)
                self.token = generate_uuid()

            def verify_password(self, pwd):
                return check_password_hash(self.password, pwd)

        self.Admin_class = Admin

        class PollTelegram(self.connDBParams_obj.db.Model):
            __tablename__ = 'polls_telegram'
            id_poll = Column('id_poll', String, ForeignKey('polls.id_poll', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
            poll_id_telegram = Column(String, primary_key=True)

            def __init__(self, id_poll, poll_id_telegram):
                self.id_poll = id_poll
                self.poll_id_telegram = poll_id_telegram

        self.PollTelegram_class = PollTelegram

        class Choice(self.connDBParams_obj.db.Model):
            __tablename__ = 'choices'
            id_poll = Column('id_poll', String, ForeignKey('polls.id_poll', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
            number = Column('number', INT, primary_key=True)
            answer = Column('answer', String)
            choice_useranswer_rel = relationship('UserAnswer', backref='Choice')  # one to many

            def __init__(self, id_poll, number, answer):
                self.id_poll = id_poll
                self.number = number
                self.answer = answer
        self.Choice_class = Choice

        class UserAnswer(self.connDBParams_obj.db.Model):
            __tablename__ = 'users_answers'
            id_user = Column('id_user', String, ForeignKey('users.id_user', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
            id_poll = Column('id_poll', String, ForeignKey('polls.id_poll', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
            number = Column('number', INT) # one user answer per poll
            __table_args__ = (
                ForeignKeyConstraint(['id_poll', 'number'], ['choices.id_poll', 'choices.number'],),
            )

            def __init__(self, id_user, id_poll, number):
                self.id_user = id_user
                self.id_poll = id_poll
                self.number = number
        self.UserAnswer_class = UserAnswer

        class AdminPoll(self.connDBParams_obj.db.Model):
            __tablename__ = 'admins_polls'
            token = Column('token', String, ForeignKey('admins.token', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
            id_poll = Column('id_poll', String, ForeignKey('polls.id_poll', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)

            def __init__(self, token, id_poll):
                self.token = token
                self.id_poll = id_poll
        self.AdminPoll_class = AdminPoll







