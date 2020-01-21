from flask import Flask, render_template, redirect, url_for, request, flash

import os

from root.dao.database import Database
from root.dao.orm.model import *

from root.forms.user import *
from root.forms.category import *
from root.forms.messenger import *
from root.forms.message import *



app = Flask(__name__)

SECRET_KEY = os.urandom(24)
app.config['SECRET_KEY'] = SECRET_KEY

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qhsmovulrcixsq:4de2d87cc269e6e20a3b9d3a3cafd5b28eb5deb674a965ccb74db00dffc5e9f8@ec2-174-129-255-11.compute-1.amazonaws.com:5432/dd8urtd5qotins'

db = Database()


Base.metadata.create_all(db.sqlalchemy_engine)
session = db.sqlalchemy_session

@app.route('/', methods = ['GET', 'POST'])
def login():

    error = None
    form = LoginForm()


    if request.method == 'POST':
        user = request.form['username']
        users = list(db.sqlalchemy_session.query(Users.display_name, Users.password).filter(
            Users.display_name == user))


        if user == 'admin' and \
                request.form['password'] == 'secret':
            return redirect(url_for('admin'))

        elif not users:
            error = 'Такой пользователь не существует: введите данные правильно или регистрируйтесь.'
        elif request.form['password'] != users[0][1]:
            error = 'Неправильный логин или пароль.'

        else:
            flash('Вы успешно ввошли!')
            return redirect(url_for('client', username=user))

    return render_template('login.html', error = error, form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register():

    error = None
    form = UserForm(request.form)


    if request.method == 'POST' and form.validate():

        user = list(db.sqlalchemy_session.query(Users.display_name, Users.password).filter(
            Users.display_name == request.form['username']))

        if user:

            error = 'Такой пользователь уже существует: придумайте другой username'
        else:

            user = Users(display_name = request.form['username'], password = request.form['password'], location = request.form['location'])
            db.createUser(user)
            flash('Спасибо за регистрацию')

            return redirect(url_for('login'))

    return render_template('userForm.html', form=form, tittle='Регистрация', error=error)


@app.route('/<username>', methods = ['GET', 'POST'])
def client(username):

    client_id = list(db.sqlalchemy_session.query(Users.user_id).filter(Users.display_name == username))[0][0]
    client_message = list(db.sqlalchemy_session.query(Message).filter(Message.user_fk == client_id))

    form = messageClientForm(request.form)
    form.messenger.choices = [(messenger.messenger_name, messenger.messenger_name) for messenger in db.sqlalchemy_session.query(Messenger).all()]
    form.category.choices = [(category.category_name, category.category_name) for category in db.sqlalchemy_session.query(Category).all()]

    if request.method == 'POST' and form.validate():
        user = list(db.sqlalchemy_session.query(Users.user_id).filter(Users.display_name==username))[0][0]
        tittle = form.tittle.data
        body = form.body.data
        messenger = list(db.sqlalchemy_session.query(Messenger.messenger_id).filter(Messenger.messenger_name==request.form['messenger']))[0][0]
        category = list(db.sqlalchemy_session.query(Category.category_id).filter(Category.category_name==request.form['category']))[0][0]

        message = Message(user_fk=user, tittle=tittle, body=body, messenger_fk=messenger, category_fk=category)
        db.createMessage(message)
        return redirect(url_for('client', username=username))

    return render_template('client.html', client=username, messages = client_message, form=form)



@app.route('/admin')
def admin():
    return render_template('admin_base.html')


@app.route('/admin/user')
def users():
    all_users = db.fetchAllUsers()
    return render_template('user.html', all_users=all_users)

@app.route('/admin/user/delete_user/<user_id>')
def delete_user(user_id):
    db.deleteUser(user_id)
    return redirect(url_for("users"))

@app.route('/admin/user/edit/<user_id>', methods = ["GET", "POST"])
def update_user(user_id):

    error = None

    user_data = db.fetchUser(user_id)

    form = UserUpdateForm(request.form, username = user_data.display_name, location = user_data.location)

    if request.method == "POST" and form.validate():

            username = form.username.data

            same_user = list(db.sqlalchemy_session.query(Users).filter(Users.display_name == request.form['username']))

            if same_user and username != user_data.display_name:
                error = 'Такой пользователь уже существует'
            else:

                if request.form['password'] == '':
                    password = user_data.password
                else:
                    password = form.password.data

                location = form.location.data

                db.updateUser(user_id, display_name=username, password=password, location=location)

                return redirect(url_for("users"))


    return render_template("userUpdateForm.html", form=form, tittle = 'Изменить пользователя', error = error)

@app.route('/admin/user/create_new_user', methods = ["GET", "POST"])
def create_user():

    error = None
    form = UserForm(request.form)


    if request.method == "POST" and form.validate():

        user = list(db.sqlalchemy_session.query(Users.display_name, Users.password).filter(
            Users.display_name == request.form['username']))

        if user:
            error = 'Такой пользователь уже существует: придумайте другой username'
        else:
            user = Users(display_name=request.form['username'], password=request.form['password'],
                         location=request.form['location'])
            db.createUser(user)

            return redirect(url_for('users'))


    return render_template('userForm.html', form=form, tittle='Создать нового пользователя', error = error)

@app.route('/admin/category')
def category():
    all_category = db.fetchAllCategory()
    return render_template('category.html', all_category=all_category)

@app.route('/admin/category/delete_category/<category_id>')
def delete_category(category_id):
    db.deleteCategory(category_id)
    return redirect(url_for("category"))
#
@app.route('/admin/category/edit/<category_id>', methods = ["GET", "POST"])
def update_category(category_id):

    error = None
    category_data = db.fetchCategory(category_id)


    form = CategoryForm(request.form,\
                        category_name = category_data.category_name,
                        amount = category_data.population_count )

    if request.method == "POST" and form.validate():

        categories = list(db.sqlalchemy_session.query(Category.category_name).
                          filter(Category.category_name == request.form['category_name']))

        if categories and request.form['category_name'] != category_data.category_name:
            error = 'Такая категория уже существует'
        else:

            category_name = form.category_name.data
            amount = form.amount.data
            db.updateCategory(category_id, category_name, amount)
            return redirect(url_for("category"))

    return render_template("categoryForm.html", form=form, tittle = 'Изменить категорию', error = error)

@app.route('/admin/category/create_new_category', methods = ["GET", "POST"])
def create_category():

    error = None

    form = CategoryForm(request.form)

    if request.method == "POST" and form.validate():

        categories = list(db.sqlalchemy_session.query(Category.category_name).
                          filter(Category.category_name == request.form['category_name']))

        if categories:
            error = 'Такая категория уже существует'
        else:
            category_name = form.category_name.data
            amount = form.amount.data
            category = Category(category_name=category_name, population_count=amount)
            db.createCategory(category)

            return redirect(url_for("category"))

    return render_template("categoryForm.html", form=form, tittle = 'Создать новую категорию', error = error)


@app.route('/admin/messenger')
def messengers():
    all_messengers = db.fetchAllMessenger()
    return render_template('messenger.html', all_messengers=all_messengers)


@app.route('/admin/messenger/delete_messenger/<messenger_id>')
def delete_messenger(messenger_id):
    db.deleteMessenger(messenger_id)
    return redirect(url_for("messengers"))

@app.route('/admin/messenger/edit_messenger/<messenger_id>', methods=['POST', 'GET'])
def update_messenger(messenger_id):
    error = None

    messenger_data = db.fetchMessenger(messenger_id)

    form = MessengerForm(request.form,
                         messenger_name=messenger_data.messenger_name)

    if request.method == 'POST' and form.validate():

        same_messenger = list(db.sqlalchemy_session.query(Messenger).
                              filter(Messenger.messenger_name == request.form['messenger_name']))
        if same_messenger and request.form['messenger_name'] != messenger_data.messenger_name:
            error = 'Такая категория уже существует'
        else:
            messenger_name = form.messenger_name.data

            db.updateMessenger(messenger_id, messenger_name)
            return redirect(url_for('messengers'))

    return render_template('messengerForm.html', form = form, tittle = 'Изменить messenger', error=error)

@app.route('/admin/messenger/create_new_messenger', methods = ["GET", "POST"])
def create_messenger():

    error = None

    form = MessengerForm(request.form)

    if request.method == "POST" and form.validate():

        same_messenger = list(db.sqlalchemy_session.query(Messenger).
                              filter(Messenger.messenger_name == request.form['messenger_name']))

        if same_messenger:
            error = 'Такая категория уже существует'
        else:
            messenger_name = form.messenger_name.data
            messenger = Messenger(messenger_name=messenger_name)
            db.createMessenger(messenger)

            return redirect(url_for("messengers"))

    return render_template("messengerForm.html", form=form, tittle = 'Создать новый messenger', error=error)

@app.route('/admin/messages')
def messages():
    all_messages = db.fetchAllMessages()
    all_users = db.fetchAllUsers()
    all_messengers = db.fetchAllMessenger()
    all_categories = db.fetchAllCategory()

    return render_template('messages.html', all_messages=all_messages, all_users = all_users, all_messengers = all_messengers, all_categories
                           =all_categories)

@app.route('/admin/messages/delete/<message_id>')
def delete_message(message_id):
    db.deleteMessage(message_id)
    return redirect(url_for('messages'))


@app.route('/admin/messages/edit/<message_id>', methods = ['POST', 'GET'])
def update_message(message_id):

    error = None

    message_data = db.fetchMessage(message_id)


    user_name = list(db.sqlalchemy_session.query(Users.display_name).filter(Users.user_id == message_data.user_fk))

    if user_name:
        user_name = user_name[0][0]
    else:
        user_name = ''

    if message_data.messenger_fk is not None:
        messenger_name = list(db.sqlalchemy_session.query(Messenger.messenger_name).filter(
            Messenger.messenger_id == message_data.messenger_fk))[0][0]
    else:
        messenger_name = None


    if message_data.category_fk is not None:
        category_name = list(db.sqlalchemy_session.query(Category.category_name).filter(
            Category.category_id == message_data.category_fk))[0][0]
    else:
        category_name = None


    form = messageUpdateForm(request.form, messenger = messenger_name, category = category_name)

    form.messenger.choices =[(messenger.messenger_name, messenger.messenger_name) for messenger in db.sqlalchemy_session.query(Messenger).all()]
    form.category.choices = [(category.category_name, category.category_name) for category in db.sqlalchemy_session.query(Category).all()]


    if request.method == 'POST' and form.validate():

        if request.form['messenger'] is None:
            messenger_id = None
        else:
            messenger_id = list(db.sqlalchemy_session.query(Messenger.messenger_id).filter(
            Messenger.messenger_name == request.form['messenger']))[0][0]

        categories = list(db.sqlalchemy_session.query(Category.category_id).filter(
            Category.category_name == request.form['category']))

        if categories:
            category_id = categories[0][0]
        else:
            category_id = None

        db.updateMessage_second(message_id=message_id, messenger = messenger_id, category = category_id)
        return redirect(url_for('messages'))

    return render_template('messageUpdateForm.html', form=form, data = message_data, user = user_name, error=error)




@app.route('/admin/messages/create_new_message', methods = ["GET", "POST"])
def create_message():

    error = []

    form = messageCreateForm(request.form)

    form.user.choices = [(user.display_name, user.display_name)
                         for user in db.sqlalchemy_session.query(Users).all()]
    form.messenger.choices = [(messenger.messenger_name, messenger.messenger_name)
                              for messenger in db.sqlalchemy_session.query(Messenger).all()]
    form.category.choices = [(category.category_name, category.category_name)
                             for category in db.sqlalchemy_session.query(Category).all()]

    if request.method == "POST" and form.validate():

        user = list(db.sqlalchemy_session.query(Users.user_id).filter(Users.display_name == request.form['user']))[0][0]
        tittle = form.tittle.data
        body = form.body.data
        messenger = list(db.sqlalchemy_session.query(Messenger.messenger_id).filter(Messenger.messenger_name == request.form['messenger']))[0][0]
        category = list(db.sqlalchemy_session.query(Category.category_id).filter(Category.category_name == request.form['category']))[0][0]

        message = Message(tittle=tittle, body=body, user_fk=user, messenger_fk=messenger, category_fk=category)
        db.createMessage(message)
        return redirect(url_for("messages"))

    return render_template("messageForm.html", form=form, tittle = 'Создать новое сообщение', error = error)

# @app.route('/dashboard')
# def dashboard():
#     # message_data = db.fetchAllMessages()
#     # messager_id = []
#     # clicks = []
#     #
#     # for message in message_data:
#     #     messager_id.append(message.messenger)
#     #     clicks.append(message.count_clicks)
#     #
#     # bar = go.Bar(
#     #     x = messager_id,
#     #     y =clicks
#     # )
#
#     catagory_data = db.fetchAllCatagory()
#     catagory_name = []
#     population = []
#
#     for catagory in catagory_data:
#         catagory_name.append(catagory.catagory_name)
#         population.append(catagory.population)
#
#     pie = go.Pie(
#         labels = catagory_name,
#         values = population
#     )
#
#     attach_data = db.fetchAllAttaches()
#     attach_name = []
#     attach_size = []
#
#     for attach in attach_data:
#         attach_name.append(attach.name)
#         attach_size.append(attach.size)
#
#     bar = go.Bar(
#         x=attach_name,
#         y=attach_size
#     )
#
#     data = {
#         "bar": [bar],
#         "pie": [pie]
#     }
#
#
#
#     graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
#     return render_template("dashboard.html", graphsJSON=graphsJSON)

if __name__ == '__main__':
    app.run(debug=True)