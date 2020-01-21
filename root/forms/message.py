from wtforms import StringField, PasswordField, Form, IntegerField
from wtforms import validators, SelectField
from wtforms.validators import Optional


class messageCreateForm(Form):
    tittle = StringField("Tittle: ",
                         [validators.Length(min=0, max=30)])
    body = StringField("Text of message: ",
                       [validators.DataRequired(),
                        validators.Length(min=1, max=300)])

    user = SelectField("User: ", choices=[], default=None)
    messenger = SelectField("Messenger: ", choices=[])
    category = SelectField("Category: ", choices=[])

class messageUpdateForm(Form):
    messenger = SelectField("Messenger: ", choices=[], validators=[Optional()])
    category = SelectField("Category: ", choices=[], default=None)


class messageClientForm(Form):
    tittle = StringField("Tittle: ",
                         [validators.Length(min=0, max=30)])
    body = StringField("Text of message: ",
                       [validators.DataRequired(),
                        validators.Length(min=1, max=300)])

    messenger = SelectField("Messenger: ", choices=[])
    category = SelectField("Category: ", choices=[])

