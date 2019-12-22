from root.entities import *
import root.credentials

import sqlalchemy as db
from sqlalchemy.orm import Session



class Database():
    cstr = 'postgresql://{user}:{password}@{hostname}/{database}'.format(
        user=root.credentials.username,
        password=root.credentials.password,
        hostname=root.credentials.host,
        database=root.credentials.database
    )
    engine = db.create_engine(cstr)

    def __init__(self):
        self.connection = self.engine.connect()
        print('DB Instance created')

    def getAttach(self):
        first = Attach(file_type='.pdf', name='name1', size='15')
        second = Attach(file_type='.txt', name='name2', size='35')
        third = Attach(file_type='.pdf', name='name3', size='15')

        session = Session(bind=self.connection)

        session.add(first)
        session.add(second)
        session.add(third)

        session.commit()

    def fetchAllAttach(self):
        self.session = Session(bind=self.connection)
        attach = self.session.query(Attach).all()
        return attach

    #-----------------------------------Users-------------------------------------


    def fetchAllUsers(self):
        self.session = Session(bind=self.connection)
        users = self.session.query(Users).all()
        return users

    def createUser(self, user):
        session = Session(bind=self.connection)
        session.add(user)
        session.commit()

    def fetchUser(self, username):
        self.session = Session(bind=self.connection)
        user = self.session.query(Users).filter(Users.username == username).first()
        return user


    def  updateUserName(self, username, first_name, second_name):
        session = Session(bind=self.connection)
        dataToUpdate = {Users.first_name: first_name, Users.second_name: second_name}
        userData = session.query(Users).filter(Users.username == username)
        userData.update(dataToUpdate)
        session.commit()


    def deleteUser(self, username):
        session = Session(bind=self.connection)
        userData = session.query(Users).filter(Users.username == username).first()
        session.delete(userData)
        session.commit()




#M------------------Messege---------------------------------------


    def fetchAllMessages(self):
        self.session = Session(bind=self.connection)
        messages = self.session.query(Message).all()
        return messages


    def create_messege(self, new_message):
        session = Session(bind=self.connection)
        session.add(new_message)
        session.commit()
        print('Messege created successfully!')


    def fetchMessage(self, messege_id):
        self.session = Session(bind=self.connection)
        message = self.session.query(Message).filter(Message.messege_id == messege_id).first()
        return message

    def updateCatagoryMessage(self, messege_id, recipient, sender, messenger, content, catagory, count_clicks):
        session = Session(bind=self.connection)
        dataToUpdate = {Message.recipient: recipient, Message.sender: sender, Message.messenger: messenger, Message.content: content, Message.catagory: catagory, Message.count_clicks: count_clicks}
        messageData = session.query(Message).filter(Message.messege_id == messege_id)
        messageData.update(dataToUpdate)
        session.commit()


    def deleteClicks(self, click_id):
        session = Session(bind=self.connection)
        ClickData = session.query(Clicks).filter(Clicks.click_id == click_id).first()
        session.delete(ClickData)
        session.commit()


    def deleteMessage(self, messege_id):
        session = Session(bind=self.connection)
        messageData = session.query(Message).filter(Message.messege_id == messege_id).first()
        session.delete(messageData)
        session.commit()



#---------------------Catagory------

    def fetchAllCatagory(self):
        self.session = Session(bind=self.connection)
        catagories = self.session.query(Catagory).all()
        return catagories

    def createCatagory(self, catagory):
        session = Session(bind=self.connection)
        session.add(catagory)
        session.commit()


    def fetchCatagory(self, catagory_name):
        self.session = Session(bind=self.connection)
        catagory = self.session.query(Catagory).filter(Catagory.catagory_name == catagory_name).first()
        return catagory

    def updateCatagoryPopulation(self, catagory_name, population):
        session = Session(bind=self.connection)
        dataToUpdate = {Catagory.population: population}
        catagoryData = session.query(Catagory).filter(Catagory.catagory_name == catagory_name)
        catagoryData.update(dataToUpdate)
        session.commit()


    def deleteCatagory(self, catagory_name):
        session = Session(bind=self.connection)
        Data = session.query(Catagory).filter(Catagory.catagory_name == catagory_name).first()
        session.delete(Data)
        session.commit()


#-----------------------ATTACH-------------------------




#
# base = Database()
#
# user = Users(username = 'ex', password = 'PASS', first_name = 'имя', second_name = 'фамилия')
# base.createUser(user)
#
#
# #
# # user = Users(username = 'Foo', password = 'password', first_name = 'имя', second_name = 'фамилия')
# # base.createUser(user)
# # base.updateUserName('Foo', 'Оля', 'Яблунева')
# for row in (base.fetchAllUser()):
#     print (row)

#
# base.deleteUser('Foo')
#
# new_mes = Message(recipient='puy-puy', sender='user1', messenger='1',content='сообщение jffh')
# base.create_messege(new_mes)



# base.updateCatagoryMessage(9, 'sport')
# base.fetchByQyery('message')
# base.deleteMessage(9)
