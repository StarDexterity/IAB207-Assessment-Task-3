from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), index=True, unique=True, primary_key=True)
    email = db.Column(db.String(100), index=True, unique=True, primary_key=True)
    contact_number = db.Column(db.Integer, unique=True, index=True, primary_key=True)
    address = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')



class Event(db.Model):
    __tablename__ = 'destinations'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    sport_type = db.Column(db.String(10))
    image = db.Column(db.String(400))
    status = db.Column(db.String(10))
    address = db.Column(db.String(50))

    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())

    email = db.Column(db.String(100), db.ForeignKey('users.email'))
    contact_number = db.Column(db.Integer, db.ForeignKey('users.contact_number'))
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='event')

    
	
    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(400))
    date_of_creation = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_name = db.Column(db.String(100), db.ForeignKey('users.user_name'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


    def __repr__(self):
        return "<Comment: {}>".format(self.text)