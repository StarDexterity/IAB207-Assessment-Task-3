
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError


#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    # indicates user should be kept logged in between sessions
    keep_loggedin = BooleanField("Stay logged in")
    submit = SubmitField("Login")

def my_length_check(form, field):
    if len(field.data) > 20:
        raise ValidationError('Username must be less than 20 characters')

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired(), my_length_check])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])

    phone_no = StringField('Phone number', validators=[InputRequired("Please enter a phone number")])
    address = StringField('Address', validators=[InputRequired("Please enter an address")])
    
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")