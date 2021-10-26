#import flask - from the package import class
from flask import Flask 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static\\img\\uploaded'


#create a function that creates a web application
# a web server will run this web application
def create_app():
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=True
    # sets the path of uploaded images
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # sets max upload size to 16 megabytes
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    
    app.secret_key='utroutoru' # secret key (Maybe move to .env in the future)
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sportdb.sqlite'
    #initialize db with flask app
    db.init_app(app)



    bootstrap = Bootstrap(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    
    return app



