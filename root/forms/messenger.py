from wtforms import StringField, PasswordField, Form
from wtforms import validators, SelectField


class MessengerForm(Form):
    messenger_name = StringField("Name: ",
                                 [validators.DataRequired(),
                                  validators.Length(min=4, max=30)])

