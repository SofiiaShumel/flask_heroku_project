from root.entities import *
import root.credentials as cr

import sqlalchemy as db
from sqlalchemy.orm import Session, sessionmaker

import psycopg2


class Database(object):

    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:
                connection = psycopg2.connect(host=cr.host, database=cr.database, user=cr.username, password=cr.password)
                cursor = connection.cursor()

                print('PostgreSQL database version:')
                cursor.execute('SELECT version()')

                db_version = cursor.fetchone()
                print(db_version)

                engine = db.create_engine(cr.DATABASE_URI)

                Session = sessionmaker(bind=engine)
                session = Session()

                Database._instance.sqlalchemy_session = session
                Database._instance.sqlalchemy_engine = engine

            except Exception as error:
                print('Error: connection not established {}'.format(error))


        return cls._instance


    def __init__(self):
        engine = db.create_engine(cr.DATABASE_URI)

        Session = sessionmaker(bind=engine)
        session = Session()

        self.sqlalchemy_session = session
        self.sqlalchemy_engine = engine



    def __del__(self):
        self.sqlalchemy_session.close()


    # cstr = 'postgresql://{user}:{password}@{hostname}/{database}'.format(
    #     user=root.credentials.username,
    #     password=root.credentials.password,
    #     hostname=root.credentials.host,
    #     database=root.credentials.database
    # )
    #
    # engine = db.create_engine(cstr,  pool_size=20, max_overflow=0)
    #
    #
    #
    # def __init__(self):
    #     # self.connection = self.engine.connect()
    #     # self.session = None
    #     # print('DB Instance created')
    #
    #     self.connection = self._instance.connection
    #     self.sqlalchemy_session = self._instance.sqlalchemy_session
    #     self.sqlalchemy_engine = self._instance.sqlalchemy_engine


    # def __enter__(self):
    #     if self.session is not None:
    #         self.session.close()
    #     self.session = self.Session()
    #     return self.session
    #
    # def __exit__(self, type, value, trace):
    #     if type is not None:
    #         print(f'Exeption happened in transaction:\n{value}')
    #         print(f'Trace:\n{trace}')
    #         self.session.rollback()
    #     else:
    #         print('transaction complete')
    #         self.session.commit()
    #     self.session.close()
    #     return True


    #-----------------------------------Users-------------------------------------


    def fetchAllUsers(self):
        # self.session = Session(bind=self.connection)
        users = self.sqlalchemy_session.query(Users).all()
        return users

    def createUser(self, user):
        # session = Session(bind=self.connection)
        self.sqlalchemy_session.add(user)
        self.sqlalchemy_session.commit()

    def fetchUser(self, username):
        # self.session = Session(bind=self.connection)
        user = self.sqlalchemy_session.query(Users).filter(Users.username == username).first()
        return user


    def  updateUserName(self, username, first_name, second_name):
        # session = Session(bind=self.connection)
        dataToUpdate = {Users.first_name: first_name, Users.second_name: second_name}
        userData = self.sqlalchemy_session.query(Users).filter(Users.username == username)
        userData.update(dataToUpdate)
        self.sqlalchemy_session.commit()


    def deleteUser(self, username):
        # session = Session(bind=self.connection)
        userData = self.sqlalchemy_session.query(Users).filter(Users.username == username).first()
        self.sqlalchemy_session.delete(userData)
        self.sqlalchemy_session.commit()




#M------------------Messege---------------------------------------


    def fetchAllMessages(self):
        # self.session = Session(bind=self.connection)
        messages = self.sqlalchemy_session.query(Message).all()
        return messages


    def create_messege(self, new_message):
        # session = Session(bind=self.connection)
        self.sqlalchemy_session.add(new_message)
        self.sqlalchemy_session.commit()


    def fetchMessage(self, messege_id):
        # self.session = Session(bind=self.connection)
        message = self.sqlalchemy_session.query(Message).filter(Message.messege_id == messege_id).first()
        return message

    def updateCatagoryMessage(self, messege_id, recipient, sender, messenger, content, catagory, count_clicks):
        # session = Session(bind=self.connection)
        dataToUpdate = {Message.recipient: recipient, Message.sender: sender, Message.messenger: messenger, Message.content: content, Message.catagory: catagory, Message.count_clicks: count_clicks}
        messageData = self.sqlalchemy_session.query(Message).filter(Message.messege_id == messege_id)
        messageData.update(dataToUpdate)
        self.sqlalchemy_session.commit()


    def deleteClicks(self, click_id):
        # session = Session(bind=self.connection)
        ClickData = self.sqlalchemy_session.query(Clicks).filter(Clicks.click_id == click_id).first()
        self.sqlalchemy_session.delete(ClickData)
        self.sqlalchemy_session.commit()


    def deleteMessage(self, messege_id):
        # session = Session(bind=self.connection)
        messageData = self.sqlalchemy_session.query(Message).filter(Message.messege_id == messege_id).first()
        self.sqlalchemy_session.delete(messageData)
        self.sqlalchemy_session.commit()



#---------------------Catagory------

    def fetchAllCatagory(self):
        # self.session = Session(bind=self.connection)
        catagories = self.sqlalchemy_session.query(Catagory).all()
        return catagories

    def createCatagory(self, catagory):
        # session = Session(bind=self.connection)
        self.sqlalchemy_session.add(catagory)
        self.sqlalchemy_session.commit()


    def fetchCatagory(self, catagory_name):
        # self.session = Session(bind=self.connection)
        catagory = self.sqlalchemy_session.query(Catagory).filter(Catagory.catagory_name == catagory_name).first()
        return catagory

    def updateCatagoryPopulation(self, catagory_name, population):
        # session = Session(bind=self.connection)
        dataToUpdate = {Catagory.population: population}
        catagoryData = self.sqlalchemy_session.query(Catagory).filter(Catagory.catagory_name == catagory_name)
        catagoryData.update(dataToUpdate)
        self.sqlalchemy_session.commit()


    def deleteCatagory(self, catagory_name):
        # session = Session(bind=self.connection)
        Data = self.sqlalchemy_session.query(Catagory).filter(Catagory.catagory_name == catagory_name).first()
        self.sqlalchemy_session.delete(Data)
        self.sqlalchemy_session.commit()
