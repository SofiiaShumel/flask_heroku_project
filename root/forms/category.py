from wtforms import StringField, Form, IntegerField
from wtforms import validators


class CategoryForm(Form):

    category_name = StringField('Name: ', [
        validators.DataRequired(),
        validators.Length(min=4, max=30)])

    amount = IntegerField('Amount: ',
        [validators.NumberRange(min=0, max=100000)])
