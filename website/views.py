import os
from datetime import datetime

from flask import Blueprint
from flask import send_from_directory
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound

from website import ALLOWED_EXTENSIONS, db

from .forms import EventForm, TestForm
from .models import Event

from . import misc

bp = Blueprint('main', __name__)

# checks if filename has an allowed file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    events = Event.query.all()
    ev:Event = events[0]
    return render_template('index.html', misc=misc, events=events)

# serves images from uploads folder
# use 'url_for("download", filename=name)' in html to use this function
@bp.route('/uploads/<filename>')
def download(filename):
    # this try catch does not work  
    try:
        return send_from_directory(os.path.join(app.root_path, app.config["UPLOAD_FOLDER"]), filename)
    except NotFound as nf:
        print('file with filename {} was not found', filename)
    

@bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        title = form.title.data
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

        user_id = current_user.user_id

        new_event = Event(title=title, description=des, sport=sport, venue=venue, address=addr, 
            start_time=start_datetime, end_time=end_datetime, status=status, 
            tickets=tickets, price=price, user_id=user_id)
        db.session.add(new_event)

        # checks for image file and authenticates it
        image_file = form.image.data
        if (image_file and allowed_file(image_file.filename)):
            filename = secure_filename(image_file.filename)
            path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
            image_file.save(path)
            new_event.image = filename

        # commit database changes    
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
