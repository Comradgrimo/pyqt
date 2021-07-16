# 1. Начать реализацию класса «Хранилище» для серверной стороны. Хранение необходимо осуществлять в базе данных.
# В качестве СУБД использовать sqlite. Для взаимодействия с БД можно применять ORM.
# Опорная схема базы данных:
# На стороне сервера БД содержит следующие таблицы:
# a) клиент:
# * логин;
# * информация.
# b) историяклиента:
# * время входа;
# * ip-адрес.
# c) списокконтактов (составляется на основании выборки всех записей с id_владельца):
# * id_владельца;
# * id_клиента.
from sqlalchemy import create_engine,Table, Column, Integer, String, MetaData,DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///sqlite3.db', echo=True)

# metadata = MetaData()
# client_table = Table('client', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('login', String),
#     Column('password', String),
#     Column('info', String)
# )
# client_history = Table('client_history', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('time', DateTime)
# )
# contact_list = Table('contact_list', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('id_master', Integer, primary_key=True),
#     Column('id_client', Integer)
# )
#
# metadata.create_all(engine)


Base = declarative_base()


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    info = Column(String)
    client_history = Column(Integer)
    contact_list = Column(Integer)


    def __init__(self, login, password, info, client_history, contact_list):
        self.login = login
        self.password = password
        self.info = info
        self.client_history = client_history
        self.contact_list = contact_list
    def __repr__(self):
        return "<Client('%s','%s', '%s', '%s', '%s')>" % (self.login, self.password, self.info, self.client_history, self.contact_list)


class ClientHistory(Base):
    __tablename__ = 'client_history'
    id = Column(Integer, primary_key=True)
    message = Column(String)
    time = Column(DateTime)

    def __init__(self, message, time):
        self.message = message
        self.time = time
    def __repr__(self):
        return "<Client_history('%s', '%s')>" % (self.message, self.time)


class ContactList(Base):
    __tablename__ = 'contact_list'
    id = Column(Integer, primary_key=True)
    id_master = Column(Integer)
    id_client = Column(Integer)

    def __init__(self, id_master, id_client):
        self.id_master = id_master
        self.id_client = id_client


    def __repr__(self):
        return "<Client('%s', '%s')>" % (self.id_master, self.id_client)
Base.metadata.create_all(engine)