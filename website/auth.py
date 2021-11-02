from flask import (
    Blueprint, flash, render_template, request, url_for, redirect, session
)
from werkzeug.security import generate_password_hash, check_password_hash
#from .models import User
from .forms import LoginForm, RegisterForm
from .models import User
from flask_login import login_user, login_required, logout_user

from . import db


# create a blueprint
bp = Blueprint('auth', __name__)

def redirect_dest(fallback):
    dest_url = request.args.get('next')
    if not dest_url:
        return redirect(fallback)
    return redirect(dest_url)



@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        username = login_form.user_name.data
        password = login_form.password.data

        if login_form.keep_loggedin.data:
            session.permanent = True

        # returns first match to username
        u1:User = User.query.filter_by(user_name=username).first()
        # if none error
        if u1 is None:
            error = 'Incorrect username'
        elif not check_password_hash(u1.password_hash, password):
            error = 'Incorrect password' 
        if error is None:
            login_user(u1)
            # redirects user to the page or resource they were trying to access or index if that page does not exist
            return redirect_dest(fallback=url_for('main.index'))
        else:
            print(error)
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')


@bp.route('/register', methods=['GET', 'POST'])  
def register():  
    error = None
    #create the form
    form = RegisterForm()
    #this line is called when the form - POST
    if form.validate_on_submit():
        print('Register form submitted')
       

        #get username, password and email from the form
        uname =form.user_name.data
        pwd = form.password.data
        email=form.email_id.data
        contact_number = form.phone_no.data


        if error is None:
            pwd_hash = generate_password_hash(pwd)
            #create a new user model object
            new_user = User(user_name=uname, password_hash=pwd_hash, email=email, contact_number=contact_number)
            db.session.add(new_user)
            db.session.commit()
            flash("Registered user successfully")
            return redirect(url_for('auth.login'))
        else:
            flash(error)

    return render_template('user.html', form=form, heading='Register')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    #flash("Logout successfully") 
    return redirect(url_for("main.index"))

