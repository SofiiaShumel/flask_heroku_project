from root.dao.database import Database
from root.dao.orm.model import *


db = Database()


Base.metadata.create_all(db.sqlalchemy_engine)

session = db.sqlalchemy_session

session.query(Users).delete()
session.query(Messenger).delete()
session.query(Category).delete()
session.query(Message).delete()

Patya = Users(display_name='Patya', password='qwerty', location='Ukraine')
Katya = Users(display_name='kate41', password='kate41', location='Germany')
User = Users(display_name='user3', password='qwerty', location='Italy')

Telegram = Messenger(messenger_name = 'Telegram')
Viber = Messenger(messenger_name = 'Viber')
Whatsapp = Messenger(messenger_name = 'Whatsapp')

Comment = Category(category_name = 'comment', population_count = 0)
Answer = Category(category_name = 'answer', population_count = 10)
Question = Category(category_name = 'question', population_count = 15)

first = Message(body = """
                        Thanks for your response Ward. I simplified everything and 
                       actually tested with a real server response as you suggested.
                        When I did this, it was still broken. 
                        I then tried to compare the difference""",
                user_fk = 3, messenger_fk = 1, category_fk = 1
                )
second = Message( tittle = 'IMPORTANT!' , body = """
                        You are using a prototype library syntax instead of jQuery. Visit the episode page,
                         and look for the code used part where both prototype and jQuery syntaxes are provided""",
                user_fk = 3, messenger_fk = 1, category_fk = 1
                )
third = Message( tittle = 'read this!' , body = """
                        Це історія про пригоди найбільшого героя свого часу — Рагнара Лодброка.
                         У серіалі показаний Рагнар зі своїм племенем братів-вікінгів і своєю сім'єю в 
                         процесі постання королем усіх племен вікінгів. """,
                 user_fk=3, messenger_fk=1, category_fk=1
                 )

session.commit()