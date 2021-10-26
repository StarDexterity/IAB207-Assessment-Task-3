from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    contact_number = db.Column(db.Integer, unique=True, index=True)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to users comments
    comments = db.relationship('Comment')

    # relation to users events
    events = db.relationship('Event')

    def get_id(self):
        return (self.user_id)



class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(2000))
    sport = db.Column(db.String(20))
    image = db.Column(db.String(400))
    venue = db.Column(db.String(50))
    address = db.Column(db.String(100))

    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())

    status = db.Column(db.String(15))
    tickets = db.Column(db.Integer())
    price = db.Column(db.Float())

    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))

    #email = db.Column(db.String(100), db.ForeignKey('user.email'))
    #contact_number = db.Column(db.Integer, db.ForeignKey('user.contact_number'))

    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    #comments = db.relationship('Comment', backref='event')

    
	
    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)


class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.String(400))
    date_of_creation = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))


    def __repr__(self):
        return "<Comment: {}>".format(self.text)