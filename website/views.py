from flask import Blueprint, render_template, url_for, session, request, flash, redirect
from website import db
from .models import Event
from flask_login import login_required
from datetime import datetime

from .forms import EventForm, TestForm

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        title = form.title.data
        image = form.image.data
        des = form.description.data
        sport = form.sport.data

        start_date = form.start_date.data
        start_time = form.start_time.data

        # merge date and time into a datetime object
        start_datetime = datetime(start_date.year, start_date.month, start_date.day, start_time.hour, start_time.minute, start_time.second)

        end_date = form.end_date.data
        end_time = form.end_time.data
        
        # merge date and time into a datetime object
        end_datetime = datetime(end_date.year, end_date.month, end_date.day, end_time.hour, end_time.minute, end_time.second)
        venue = form.venue.data

        # get address information from each input
        street = form.street.data
        city = form.city.data
        state = form.state.data
        postcode = form.postcode.data

        # join address information into a single entry
        addr = ','.join([street, city, postcode, state])

        status = form.status.data
        tickets = form.tickets.data
        price = form.price.data

        new_event = Event(title=title, image=image, description=des, sport=sport, venue=venue, address=addr, 
            start_time=start_datetime, end_time=end_datetime, status=status, tickets=tickets, price=price)
        db.session.add(new_event)
        db.session.commit()
        flash("Registered event successfully")
        return redirect(url_for('main.create_event'))
    return render_template('create_event.html', form=form)

# convenience method for testing things
@bp.route('/test', methods=['GET', 'POST'])
def test():
    form = TestForm()
    if form.is_submitted():
        print(form.message.data)
    return render_template('test.html')
    

@bp.route('/booked-events')
def booked_events():
    return render_template('booked_events.html')


@bp.route('/view-details')
def view_details():
    return render_template('view_details.html')
