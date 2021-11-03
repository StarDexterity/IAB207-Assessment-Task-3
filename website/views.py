import os
from datetime import datetime

from flask import Blueprint
from flask import send_from_directory
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_url 
import flask_login
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound

from website import ALLOWED_EXTENSIONS, db
from .forms import EventForm, CommentForm, OrderForm
from .models import Event, Comment, Order


bp = Blueprint('main', __name__)

# checks if filename has an allowed file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

# serves images from uploads folder
# use 'url_for("download", filename=name)' in html to use this function
@bp.route('/uploads/<filename>')
@bp.route('/uploads')
def download(filename=None):
    if filename is not None:
        try:
            return send_from_directory(os.path.join(app.root_path, app.config["UPLOAD_FOLDER"]), filename)
        except NotFound as nf:
            print('file with filename %s was not found', filename)
            return send_from_directory(os.path.join(app.root_path, 'static\\img'), 'no_image.png')
    else:
        return send_from_directory(os.path.join(app.root_path, 'static\\img'), 'no_image.png')
    

@bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        # form was submitted and input was validated
        title = form.title.data
        des = form.description.data
        sport = form.sport.data


        # merge date and time into a datetime object
        start_date = form.start_date.data
        start_time = form.start_time.data
        start_datetime = datetime(start_date.year, start_date.month, start_date.day, start_time.hour, start_time.minute, start_time.second)
        
        # merge date and time into a datetime object
        end_date = form.end_date.data
        end_time = form.end_time.data
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
        ticket_quantity = form.ticket_quantity.data
        price = form.price.data

        user_id = current_user.user_id

        new_event = Event(title=title, description=des, sport=sport, venue=venue, address=addr, 
            start_time=start_datetime, end_time=end_datetime, status=status, 
            ticket_quantity=ticket_quantity, price=price, user_id=user_id)
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

        # let the user know the action was successful and take them to the manage events page so they can verify their event was created
        flash("Registered event successfully")
        return redirect(url_for('main.manage_events'))
    return render_template('create_event.html', form=form)

    
@bp.route('/manage-events')
@login_required
def manage_events():
    return render_template('manage_events.html', events=current_user.events)

@bp.route('/booked-events')
def booked_events():
    return render_template('booked_events.html')


@bp.route('/view-details/<event_id>', methods=['GET', 'POST'])
def view_details(event_id):
    event:Event = Event.query.filter_by(event_id=event_id).first()
    cform = CommentForm()
    oform = OrderForm()
    oform.max = event.tickets_remaining
    if cform.validate_on_submit():
        text = cform.text.data
        user_id = current_user.user_id
        new_comment = Comment(text=text, user_id=user_id, event_id=event_id, date_of_creation=datetime.now())
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('main.view_details', event_id=event_id))

    if oform.is_submitted():
        if oform.validate():
            user_id = current_user.user_id
            new_order = Order()
            db.session.add(new_order)
            db.session.commit()
            return redirect(url_for('main.booked_events'))
        else:
            flash('Order attempt was unsuccessful')
    return render_template('view_details.html', event=event, oform=oform, cform=cform)


@bp.route('/delete_event/<event_id>')
def delete_event(event_id):
    event:Event = Event.query.filter_by(event_id=event_id).first()
    if event is not None and event.is_owner:
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('main.manage_events'))
    
    
@bp.route('/edit_event/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event:Event = Event.query.filter_by(event_id=event_id).first()
    if event is not None and event.is_owner:
        form = EventForm(obj=event)
        if form.validate_on_submit():
            # populate event object with form data
            form.populate_event(event)
            db.session.commit()
            return redirect(url_for('main.manage_events'))
        
        form.start_time.data = event.start_time.time()
        form.start_date.data = event.start_time.date()
        form.end_time.data = event.end_time.time()
        form.end_date.data = event.end_time.date()

        street, city, postcode, state = event.address.split(',')
        form.street.data = street
        form.city.data = city
        form.postcode.data = postcode
        form.state.data = state
        return render_template('create_event.html', form=form)




# function for testing any html file in templates
@bp.route('/test-render/<file>')
def test_render(file):
    return render_template(file)

