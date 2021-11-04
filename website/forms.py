import re
from datetime import datetime

from flask import session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields import (BooleanField, DateField, FloatField, IntegerField,
                            PasswordField, SelectField, StringField,
                            SubmitField, TextAreaField, TimeField)
from wtforms.validators import (Email, EqualTo, InputRequired, Length,
                                ValidationError)

from .misc import get_current_event
from .models import BOOKED, CANCELLED, Event, User, sports, statuses

ALL = 'All'

#creates the login information
class LoginForm(FlaskForm):
    username=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    # indicates user should be kept logged in between sessions
    keep_loggedin = BooleanField("Stay logged in")


    submit = SubmitField("Login")

class SearchForm(FlaskForm):
    category = SelectField(choices=['All'] + sports, validators=[InputRequired()])
    search=StringField("Search")

    submit = SubmitField("Search")



 # this is the registration form
class RegisterForm(FlaskForm):
    # user name
    username=StringField("User Name", validators=[InputRequired("Please enter a username"), Length(max=20, message='Username must be no longer than 20 characters.')])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])

    phone_no = StringField('Phone number', validators=[InputRequired("Please enter a phone number")])
    address = StringField('Address', validators=[InputRequired("Please enter a address")])

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
    title = StringField(validators=[InputRequired(), Length(max=25)])
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
    address = StringField()

    status = SelectField(choices=statuses, validators=[InputRequired()])
    tickets_total = IntegerField(validators=[InputRequired()])
    price = FloatField(validators=[InputRequired()])

    is_editing = False

    submit = SubmitField('Submit')


    def validate_tickets_total(form, field):
        event:Event = get_current_event()
        if form.is_editing:
            if field.data < event.tickets_sold:
                raise ValidationError('Number must be at least {}, the number of tickets already sold.'.format(event.tickets_sold))

    def validate_address(form, field):
        if form.address.data == '' and form.venue.data == '':
            raise ValidationError('Venue or address field required')
        
        
    def populate_event(self, event:Event):
        event.title = self.title.data
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

        # join address information into a single entry
        event.addr = self.address.data

        event.status = self.status.data
        event.price = self.price.data
        event.tickets_total = self.tickets_total.data

    

class CommentForm(FlaskForm):
    text = TextAreaField(label='', validators=[InputRequired(), Length(max=400)])

class OrderForm(FlaskForm):
    ticket_quantity = IntegerField(label='', validators=[InputRequired()])

    def validate_ticket_quantity(form, field):
        event:Event = get_current_event()
        if event.status == BOOKED:
            raise ValidationError(message='Event is fully booked')
        elif event.status == CANCELLED:
            raise ValidationError('Event has been cancelled')
        elif field.data > event.tickets_remaining:
            raise ValidationError(message='Ticket quantity must be at most {}'.format(event.tickets_remaining))
        


# misc test form
class TestForm(FlaskForm):
    message = StringField()



