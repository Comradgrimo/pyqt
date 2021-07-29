
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:///sqlite3.db', echo=True)
Base = declarative_base()


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    password = Column(String)
    info = Column(String)
    message = Column(ForeignKey('message.id'))
    contact_list = Column(ForeignKey('contact_list.id'))

    def __init__(self, login, password, info, contact_list, message):
        self.login = login
        self.password = password
        self.info = info
        self.message = message
        self.contact_list = contact_list

    def __repr__(self):
        return "<Client('%s','%s', '%s', '%s', '%s')>" % (self.login, self.password, self.info, self.message, self.contact_list)


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_client = Column(ForeignKey('client.id'))
    datetime = Column(DateTime)
    content = Column(String)

    def __init__(self, id_client, datetime, content):
        self.id_client = id_client
        self.datetime = datetime
        self.content = content

    def __repr__(self):
        return "<Client_history('%s', '%s', '%s')>" % (self.message, self.datetime, self.content)


class ContactList(Base):
    __tablename__ = 'contact_list'
    id = Column(Integer, primary_key=True)
    id_master = Column(ForeignKey('client.id'))
    id_slave = Column(ForeignKey('client.id'))

    def __init__(self, id_master, id_slave):
        self.id_master = id_master
        self.id_slave = id_slave

    def __repr__(self):
        return "<Client('%s', '%s')>" % (self.id_master, self.id_slave)


Base.metadata.create_all(engine)
