from root.dao.orm.model import *
import root.dao.credentials as cr

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker


class Database(object):

    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:

                engine = db.create_engine(cr.DATABASE_URI)

                Session = sessionmaker(bind=engine)
                session = Session()

                Database._instance.sqlalchemy_session = session
                Database._instance.sqlalchemy_engine = engine

            except Exception as error:
                print('Error: connection not established {}'.format(error))

        return cls._instance


    def __init__(self):
        self.sqlalchemy_session = self._instance.sqlalchemy_session
        self.sqlalchemy_engine = self._instance.sqlalchemy_engine



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
        users = self.sqlalchemy_session.query(Users).all()
        return users

    def createUser(self, user):
        self.sqlalchemy_session.add(user)
        self.sqlalchemy_session.commit()

    def fetchUser(self, user_id):
        user = self.sqlalchemy_session.query(Users).filter(Users.user_id == user_id).first()
        return user

    def  updateUser(self, user_id, display_name, password, location):
        dataToUpdate = {Users.password: password, Users.display_name: display_name, Users.location: location}
        userData = self.sqlalchemy_session.query(Users).filter(Users.user_id == user_id)
        userData.update(dataToUpdate)
        self.sqlalchemy_session.commit()

    def deleteUser(self, user_id):
        userData = self.sqlalchemy_session.query(Users).filter(Users.user_id == user_id).first()
        self.sqlalchemy_session.delete(userData)
        self.sqlalchemy_session.commit()

#----------------------Messenger-----------------------

    def fetchAllMessenger(self):
        messengers = self.sqlalchemy_session.query(Messenger).all()
        return messengers

    def createMessenger(self, messenger):
        self.sqlalchemy_session.add(messenger)
        self.sqlalchemy_session.commit()

    def fetchMessenger(self, messenger_id):
        messenger = self.sqlalchemy_session.query(Messenger).filter(Messenger.messenger_id == messenger_id).first()
        return messenger

    def updateMessenger(self, messenger_id, messenger_name):
        dataToUpdate = {Messenger.messenger_name: messenger_name}
        messengerData = self.sqlalchemy_session.query(Messenger).filter(Messenger.messenger_id == messenger_id)
        messengerData.update(dataToUpdate)
        self.sqlalchemy_session.commit()

    def deleteMessenger(self, messenger_id):
        messengerData = self.sqlalchemy_session.query(Messenger).filter(Messenger.messenger_id == messenger_id).first()
        self.sqlalchemy_session.delete(messengerData)
        self.sqlalchemy_session.commit()



# ---------------------Category------

    def fetchAllCategory(self):
        catagories = self.sqlalchemy_session.query(Category).all()
        return catagories

    def createCategory(self, category):
        self.sqlalchemy_session.add(category)
        self.sqlalchemy_session.commit()

    def fetchCategory(self, category_id):
        category = self.sqlalchemy_session.query(Category).filter(Category.category_id == category_id).first()
        return category

    def updateCategory(self, category_id, category_name, population_count):
        dataToUpdate = {Category.category_name: category_name, Category.population_count: population_count}
        categoryData = self.sqlalchemy_session.query(Category).filter(Category.category_id == category_id)
        categoryData.update(dataToUpdate)
        self.sqlalchemy_session.commit()

    def deleteCategory(self, category_id):
        categoryData = self.sqlalchemy_session.query(Category).filter(Category.category_id == category_id).first()
        self.sqlalchemy_session.delete(categoryData)
        self.sqlalchemy_session.commit()



#-----------------------MESSAGE-----------------------


    def fetchAllMessages(self):
        messages = self.sqlalchemy_session.query(Message).all()
        return messages

    def createMessage(self, message):
        self.sqlalchemy_session.add(message)
        self.sqlalchemy_session.commit()

    def fetchMessage(self, message_id):
        message = self.sqlalchemy_session.query(Message).filter(Message.message_id == message_id).first()
        return message

    def updateMessage_first(self, message_id, tittle, body):
        dataToUpdate = {Message.tittle: tittle, Message.body: body}
        messageData = self.sqlalchemy_session.query(Message).filter(Message.message_id == message_id)
        messageData.update(dataToUpdate)
        self.sqlalchemy_session.commit()

    def updateMessage_second(self, message_id, messenger, category):
        dataToUpdate = {Message.messenger_fk: messenger, Message.category_fk: category}
        messageData = self.sqlalchemy_session.query(Message).filter(Message.message_id == message_id)
        messageData.update(dataToUpdate)
        self.sqlalchemy_session.commit()

    def deleteMessage(self, message_id):
        messageData = self.sqlalchemy_session.query(Message).filter(Message.message_id == message_id).first()
        self.sqlalchemy_session.delete(messageData)
        self.sqlalchemy_session.commit()


#--------ADITIONS--------

    def createRelationUserMessenger(self, relation):
        self.sqlalchemy_session.add(relation)
        self.sqlalchemy_session.commit()