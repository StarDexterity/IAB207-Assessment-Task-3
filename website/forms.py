from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields import (
    TextAreaField,SubmitField, StringField, PasswordField, 
    BooleanField, IntegerField, TimeField, DateField, 
    FloatField, SelectField
)
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.widgets.core import Input
import re
from .models import User, Event
from datetime import datetime


from .models import statuses, sports



#creates the login information
class LoginForm(FlaskForm):
    username=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    # indicates user should be kept logged in between sessions
    keep_loggedin = BooleanField("Stay logged in")


    submit = SubmitField("Login")





 # this is the registration form
class RegisterForm(FlaskForm):
    # user name
    username=StringField("User Name", validators=[InputRequired("Please enter a username"), Length(max=20, message='Username must be no longer than 20 characters.')])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])

    phone_no = StringField('Phone number', validators=[InputRequired("Please enter a phone number")])
    
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match"), Length(min=8, message='Password must be atleast 8 characters long')])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

    def validate_phone_no(form, field):
        if len(field.data) != 10:
            raise ValidationError('Phone number must be 10 digits')
        elif re.search('\D', field.data) is not None:
            raise ValidationError('Phone number must not contain non numerical characters')
        elif User.query.filter_by(contact_number=field.data).first():
            raise ValidationError('Phone number taken')

    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first() is not None:
            return ValidationError('Username taken')

    def validate_email_id(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email taken')






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
    description = TextAreaField(validators=[InputRequired(), Length(min=300)])
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
    ticket_quantity = IntegerField(validators=[InputRequired()])
    price = FloatField(validators=[InputRequired()])

    submit = SubmitField('Submit')

    def populate_event(self, event:Event):
        event.title = self.title.data
        event.image = self.image.data
        event.description = self.description.data
        event.sport = self.sport.data


        event.venue = self.venue.data
        # merge date and time into a datetime object
        start_date = self.start_date.data
        start_time = self.start_time.data
        event.start_time = datetime(start_date.year, start_date.month, start_date.day, start_time.hour, start_time.minute, start_time.second)
        
        # merge date and time into a datetime object
        end_date = self.end_date.data
        end_time = self.end_time.data
        event.end_time = datetime(end_date.year, end_date.month, end_date.day, end_time.hour, end_time.minute, end_time.second)

        # get address information from each input
        street = self.street.data
        city = self.city.data
        state = self.state.data
        postcode = self.postcode.data

        # join address information into a single entry
        event.addr = ','.join([street, city, postcode, state])

        event.status = self.status.data
        event.price = self.price.data
        event.tickets_total = self.ticket_quantity.data

    

class CommentForm(FlaskForm):
    text = TextAreaField(label='', validators=[InputRequired(), Length(max=400)])

class OrderForm(FlaskForm):
    ticket_quantity = IntegerField(label='')


    