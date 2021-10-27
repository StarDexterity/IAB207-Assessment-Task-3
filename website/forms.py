from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields import (
    TextAreaField,SubmitField, StringField, PasswordField, 
    BooleanField, IntegerField, TimeField, DateField, 
    FloatField, SelectField
)
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets.core import Input


# list of sports used by the application
sports = [
    'Soccer',
    'Football',
    'Netball',
    'Basketball',
    'Hockey'    
]

# list of statuses used by the application
# These might have to be relocated later to a more appropriate spot
statuses = [
    'Upcoming',
    'Inactive',
    'Booked',
    'Cancelled'
]


#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    # indicates user should be kept logged in between sessions
    keep_loggedin = BooleanField("Stay logged in")
    submit = SubmitField("Login")

def username_length_check(form, field):
    if len(field.data) > 20:
        raise ValidationError('Username must be less than 20 characters')

def phone_length_check(form, field):
    if len(field.data) != 10:
        raise ValidationError('Phone number must be 10 digits')

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired("Please enter a username"), username_length_check])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])

    phone_no = StringField('Phone number', validators=[InputRequired("Please enter a phone number"), phone_length_check])
    
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

'''
This is the Event form, used to create a new event
This class itself is not used to generate a bootstrap form, like the other Form classes
Simply to convert the values into their appropriate datatypes
NOTE: 
    If data is missing, double check html inputs name attribute and the Flask fields name are the same
    E.g.
    title = StringField() >>> <input type="text" name="title"/>
'''
class EventForm(FlaskForm):
    # title of the event, thumbnail/details image, a description of the event, and the sport the event is
    title = StringField(validators=[InputRequired()])
    image = FileField(validators=[])
    description = TextAreaField(validators=[])
    sport = SelectField(choices=sports, validators=[InputRequired()])

    # date and time information
    start_time = TimeField(validators=[InputRequired()])
    start_date = DateField(validators=[InputRequired()])
    
    end_time = TimeField(validators=[InputRequired()])
    end_date = DateField(validators=[InputRequired()])

    # address information
    venue = StringField()
    street = StringField(validators=[InputRequired()])
    city = StringField(validators=[InputRequired()])
    state = StringField(validators=[InputRequired()])
    postcode = StringField(validators=[InputRequired()])

    status = SelectField(choices=statuses, validators=[InputRequired()])
    tickets = IntegerField(validators=[InputRequired()])
    price = FloatField(validators=[InputRequired()])

class CommentForm(FlaskForm):
    text = TextAreaField(validators=[InputRequired()])


# misc test form
class TestForm(FlaskForm):
    message = StringField()