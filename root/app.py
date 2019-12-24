from flask import Flask, render_template, url_for, request
from werkzeug.utils import redirect

import json
import plotly
import plotly.graph_objs as go
import plotly.express as px

import os

from root.database import Database
from root.forms import *
from root.entities import *

app = Flask(__name__)

SECRET_KEY = os.urandom(24)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qhsmovulrcixsq:4de2d87cc269e6e20a3b9d3a3cafd5b28eb5deb674a965ccb74db00dffc5e9f8@ec2-174-129-255-11.compute-1.amazonaws.com:5432/dd8urtd5qotins'

db = Database()


Base.metadata.create_all(db.sqlalchemy_engine)

session = db.sqlalchemy_session




@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    # message_data = db.fetchAllMessages()
    # messager_id = []
    # clicks = []
    #
    # for message in message_data:
    #     messager_id.append(message.messenger)
    #     clicks.append(message.count_clicks)
    #
    # bar = go.Bar(
    #     x = messager_id,
    #     y =clicks
    # )

    catagory_data = db.fetchAllCatagory()
    catagory_name = []
    population = []

    for catagory in catagory_data:
        catagory_name.append(catagory.catagory_name)
        population.append(catagory.population)

    pie = go.Pie(
        labels = catagory_name,
        values = population
    )

    attach_data = db.fetchAllAttaches()
    attach_name = []
    attach_size = []

    for attach in attach_data:
        attach_name.append(attach.name)
        attach_size.append(attach.size)

    bar = go.Bar(
        x=attach_name,
        y=attach_size
    )

    data = {
        "bar": [bar],
        "pie": [pie]
    }



    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("dashboard.html", graphsJSON=graphsJSON)







@app.route('/user')
def users():
    all_users = db.fetchAllUsers()
    return render_template('user.html', all_users=all_users)

@app.route('/user/delete_user/<username>')
def delete_user(username):
    db.deleteUser(username)
    return redirect(url_for("users"))

@app.route('/user/edit/<username>', methods = ["GET", "POST"])
def update_user(username):
    user_data = db.fetchUser(username)
    form = UpdateUserForm(first_name=user_data.first_name,
                          second_name=user_data.second_name)

    if request.method == "POST":
        first_name = form.first_name.data
        second_name = form.second_name.data
        db.updateUserName(username, first_name, second_name)
        return redirect(url_for("users"))

    return render_template("UpdateUser.html", form=form)


@app.route('/user/create_new_user', methods = ["GET", "POST"])
def create_user():
    form = UserForm()

    if request.method == "POST":
        if not form.validate():
            return render_template("CreateUser.html", form=form)
        else:
            username = form.username.data
            password = form.password.data
            first_name = form.first_name.data
            second_name = form.second_name.data
            user = Users(username=username, password=password, first_name=first_name, second_name=second_name)
            db.createUser(user)
            return redirect(url_for("users"))
    return render_template("CreateUser.html", form=form)



#----------CATAGORY---------------
@app.route('/catagory')
def catagory():
    all_catagory = db.fetchAllCatagory()
    return render_template('catagory.html', all_catagory=all_catagory)

@app.route('/catagory/delete_catagory/<catagory_name>')
def delete_catagory(catagory_name):
    db.deleteCatagory(catagory_name)
    return redirect(url_for("catagory"))

@app.route('/catagory/edit/<catagory_name>', methods = ["GET", "POST"])
def update_catagory(catagory_name):
    catagory_data = db.fetchCatagory(catagory_name)
    form = UpdateCatagoryForm(population=catagory_data.population)

    if request.method == "POST":
        population = form.population.data
        db.updateCatagoryPopulation(catagory_name, population)
        return redirect(url_for("catagory"))

    return render_template("UpdateCatagory.html", form=form)


@app.route('/catagory/create_new_catagory', methods = ["GET", "POST"])
def create_catagory():
    form = CatagoryForm()

    if request.method == "POST":
        if not form.validate():
            return render_template("CreateCatagory.html", form=form)
        else:
            catagory_name = form.catagory_name.data
            population = form.population.data
            catagory = Catagory(catagory_name=catagory_name, population=population)
            db.createCatagory(catagory)
            return redirect(url_for("catagory"))
    return render_template("CreateCatagory.html", form=form)

#--------MESSAGE----------------------------------------------

@app.route('/messages')
def messages():
    all_messages = db.fetchAllMessages()
    return render_template('messages.html', all_messages=all_messages)

@app.route('/messages/delete_message/<message_id>')
def delete_message(message_id):
    db.deleteMessage(message_id)
    return redirect(url_for('messages'))

@app.route('/messages/edit/<message_id>', methods = ["GET", "POST"])
def update_message(message_id):
    message_data = db.fetchMessage(message_id)
    form = MessageForm(recipient=message_data.recipient,
                          sender=message_data.sender,
                       messenger=message_data.messenger,
                       content=message_data.content,
                       catagory=message_data.catagory,
                       count_clicks=message_data.count_clicks)

    if request.method == "POST":
        recipient = form.recipient.data
        sender = form.sender.data
        messenger = form.messenger.data
        content = form.content.data
        catagory = form.catagory.data
        count_clicks = form.count_clicks.data

        db.updateCatagoryMessage(message_id, recipient, sender, messenger, content, catagory, count_clicks)
        return redirect(url_for("messages"))

    return render_template("UpdateMessage.html", form=form)


@app.route('/messages/create_new_message', methods = ["GET", "POST"])
def create_message():
    form = MessageForm()

    if request.method == "POST":
        if not form.validate():
            return render_template("CreateMessage.html", form=form)
        else:
            recipient = form.recipient.data
            sender = form.sender.data
            messenger = form.messenger.data
            content = form.content.data
            catagory = form.catagory.data
            count_clicks = form.count_clicks.data


            message = Message(recipient=recipient, sender=sender, messenger=messenger, content=content, catagory=catagory, count_clicks=count_clicks )
            db.create_messege(message)
            return redirect(url_for("messages"))
    return render_template("CreateMessage.html", form=form)


#-------TASK--------

@app.route('/get')
def get_new():
    first = Attach(file_type = '.pdf', name = 'pic1', size = '15')
    second = Attach(file_type = '.pdf', name = 'pic2', size = '20')
    third = Attach(file_type = '.txt', name = 'cur', size = '50')
    db.addAttach(first)
    db.addAttach(second)
    db.addAttach(third)
    return 'Succesfull!'

@app.route('/show')
def attaches():
    all_attaches = db.fetchAllAttaches()
    return render_template('attach.html', all_attaches=all_attaches)

@app.route('/create_attache')
def create_attach():
    form = AttachForm()

    if request.method == "POST":
        if not form.validate():
            return render_template("CreateAttach.html", form=form)
        else:
            file_type = form.file_type.data
            name = form.name.data
            size = form.size.data

            attach = Attach(file_type=file_type, name=name, size=size)
            db.addAttach(attach)
            return redirect(url_for("attaches"))
    return render_template("CreateAttach.html", form=form)



if __name__ == '__main__':
    app.run(debug=True)