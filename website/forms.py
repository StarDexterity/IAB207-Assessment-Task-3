
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, BooleanField, IntegerField, TimeField, DateField, FloatField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError


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
    #if len(field.data) != 10:
    #    raise ValidationError('Phone number must be 10 digits')
    # !!! sorry for commenting out, just having trouble with this code
    pass

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired("Please enter a username"), username_length_check])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])

    phone_no = StringField('Phone number', validators=[InputRequired("Please enter a phone number"), phone_length_check])
    
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
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
    title = StringField()

    image = StringField()

    description = TextAreaField()

    sport = IntegerField()

    # date and time information
    start_time = TimeField()
    start_date = DateField()
    
    end_time = TimeField()
    end_date = DateField()

    # adress information
    venue = StringField()
    street_name = StringField()
    city = StringField()
    state = StringField()

    status = IntegerField()
    tickets = IntegerField()
    price = FloatField()


# misc test form
class TestForm(FlaskForm):
    message = StringField()
