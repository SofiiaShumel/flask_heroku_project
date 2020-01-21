from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP
import datetime

Base = declarative_base()

UsersMessengers = Table('association', Base.metadata,
                        Column('user', Integer, ForeignKey('users.user_id')),
                        Column('messenger', Integer, ForeignKey('messenger.messenger_id')))



class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    display_name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    location = Column(String)

    messages = relationship('Message', back_populates='user')

    messengers = relationship("Messenger", secondary=UsersMessengers, back_populates='users')



class Messenger(Base):
    __tablename__ = 'messenger'
    messenger_id = Column(Integer, primary_key=True)
    messenger_name = Column(String, unique=True, nullable=False)

    messages = relationship('Message', back_populates='messenger')
    users = relationship("Users", secondary=UsersMessengers, back_populates='messengers')

class Category(Base):
    __tablename__= 'category'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, unique=True, nullable=False)
    population_count = Column(Integer, CheckConstraint('population_count>=0'))

    messages = relationship('Message', back_populates = 'category')


class Message(Base):
    __tablename__ = 'message'
    message_id = Column(Integer, primary_key=True)
    tittle = Column(String)
    body = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)

    user_fk = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('Users', back_populates='messages')

    messenger_fk = Column(Integer, ForeignKey('messenger.messenger_id'))
    messenger = relationship('Messenger', back_populates='messages')

    category_fk = Column(Integer, ForeignKey('category.category_id'))
    category = relationship('Category', back_populates = 'messages')







