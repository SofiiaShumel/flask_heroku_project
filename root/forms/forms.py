from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, NumberRange

class UserForm(FlaskForm):
    username = StringField('Username',
            validators=[InputRequired()])


    def validate_name (form, field):
        if len(field.data) > 20:
            raise ValidationError('Username must be less than 20 character')
    password = PasswordField('Password',

            validators=[DataRequired()])
    first_name = StringField('First Name',
            validators=[DataRequired(), Length(min=2, max=30)])
    second_name = StringField('Second Name',
            validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Submit')

class UpdateUserForm(FlaskForm):
    first_name = StringField('First Name',
            validators=[DataRequired()])
    second_name = StringField('Second Name',
            validators=[DataRequired()])
    submit = SubmitField('Submit')



class MessageForm(FlaskForm):
    recipient = StringField('Recipient', validators=[DataRequired()])
    sender = StringField('Sender', validators=[DataRequired()])
    messenger = StringField('Messenger', validators=[DataRequired()])
    content = StringField(validators=[DataRequired()])
    catagory = StringField('Catagory', validators=[DataRequired()])
    count_clicks = IntegerField('Count of clicks', validators=[DataRequired()])

    Submit = SubmitField('Submit')


class CatagoryForm(FlaskForm):
    catagory_name = StringField('Catagory name', validators=[DataRequired()])
    population = IntegerField('Population', validators=[DataRequired()])

    Submit = SubmitField('Submit')

    def validate(self):
        if float(self.population.data) < 0:
            raise ValidationError("Population more than 0")
            return False
        return True


class UpdateCatagoryForm(FlaskForm):
    population = IntegerField('Population',
            validators=[DataRequired()])
    Submit = SubmitField('Submit')


class AttachForm(FlaskForm):
    file_type = StringField('File type', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    size = IntegerField('Size', validators=[DataRequired()])

    submit = SubmitField('Submit')
