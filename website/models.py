from . import db
from flask_login import UserMixin, current_user
    
class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    contact_number = db.Column(db.Integer, unique=True, index=True)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to user's comments
    comments = db.relationship('Comment')

    # relation to user's events
    events = db.relationship('Event')

    # relation to user's orders
    orders = db.relationship('Order')

    def get_id(self):
        return (self.user_id)



class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(2000))
    sport = db.Column(db.String(20))
    image = db.Column(db.String(100))
    venue = db.Column(db.String(50))
    address = db.Column(db.String(150))

    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())

    status = db.Column(db.String(15))
    ticket_quantity = db.Column(db.Integer())
    price = db.Column(db.Float())

    user_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))

    # relation to event's orders
    orders = db.relationship('Order')


    # relation to event's comments
    comments = db.relationship('Comment')


    @property
    def is_owner(self) -> bool:
        return (self.user == current_user)


    @property
    def user(self) -> User:
        return User.query.filter_by(user_id=self.user_id).first()

    @property
    def tickets_sold(self) -> str:
        tickets_sold = 0
        for order in self.orders:
            tickets_sold += order.ticket_quantity
        return str(tickets_sold)

    
	
    def __repr__(self): #string print method
        return "<Name: {}>".format(self.title)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_quantity = db.Column(db.Integer())
    order_date = db.Column(db.DateTime())
    total_cost = db.Column(db.Float())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

    @property
    def user(self) -> User:
        return User.query.filter_by(user_id=self.user_id).first()

    @property
    def event(self) -> Event:
        return User.query.filter_by(user_id=self.user_id).first()


class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(400))
    date_of_creation = db.Column(db.DateTime)
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

    @property
    def user(self) -> User:
        return User.query.filter_by(user_id=self.user_id).first()

    @property
    def event(self) -> Event:
        return User.query.filter_by(user_id=self.user_id).first()

    def __repr__(self):
        return "<Comment: {}>".format(self.text)