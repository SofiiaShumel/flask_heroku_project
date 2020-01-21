from wtforms import StringField, PasswordField, Form
from wtforms import validators, SelectField

import pycountry


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


class UserForm(Form):

    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=30, message='Должно быть от 4 до 30 символов')])

    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6, max=20, message='Пароль должен быть больше 6 символов'),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ])

    confirm = PasswordField('Repeat Password')

    location = SelectField("Country", choices=[(country.name, country.name) for country in pycountry.countries])



class UserUpdateForm(Form):

    username = StringField('Username', [validators.DataRequired(),
                                        validators.Length(min=4, max=30)])

    password = PasswordField('Password', [
        validators.Optional(),
        validators.Length(min=6, max=20, message='Пароль должен быть больше 6 символов')
    ])

    location = SelectField("Country", choices=[(country.name, country.name) for country in pycountry.countries])



