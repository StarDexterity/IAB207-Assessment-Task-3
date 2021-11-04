import os
from datetime import datetime

from flask import Blueprint
from flask import send_from_directory
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for, abort
from flask_login import current_user, login_required, login_url
from sqlalchemy import and_, or_
from werkzeug.utils import secure_filename

from website import ALLOWED_EXTENSIONS, db
from .forms import EventForm, CommentForm, OrderForm, SearchForm
from .models import User, Event, Comment, Order
from .models import BOOKED, UPCOMING, INACTIVE, CANCELLED, ALL
from .misc import set_current_event


bp = Blueprint('main', __name__)

# error handlers for returning a custom error page when something goes wrong
@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@bp.errorhandler(500)
def not_found_error(error):
    return render_template('500.html'), 500


# checks if filename has an allowed file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    category = form.category.data
    search = '%{}%'.format(form.search.data)
    error = None
    anything_found = 'Nothing is currently within the application please add an event or wait for new events to be added'
    passed = 0

    events = Event.query.all()
    c1:Event = Event.query.filter_by(sport=category).first()

    
    # if category is all make this query else make a query with an additional check for category
    s1 = None
    if category == ALL:
        s1:Event = Event.query.filter(or_(Event.title.like(search), User.username.like(search))).all()
    else:
        s1:Event = Event.query.filter(and_(or_(Event.title.like(search), User.username.like(search)), Event.title.like(category))).all()

    if s1 is None:
        # do something
        pass
    s2:User = User.query.filter(User.username.like(search)).first()

    events = Event.query.all()

    #if search empty but category chosen find those events
    if ((category == 'All') or (c1 is not None)) and (search == ''):
        if category == 'All':
            events = Event.query.all()
            passed = 1
            anything_found = ''
        elif (c1 is not None):
            events = Event.query.filter_by(sport=category).all()
            passed = 1
            anything_found = ''

    #if search filled and found and category = all
    elif (category == 'All') and ((s1 is not None) or (s2 is not None)):
        if (s1 is not None):
            events = Event.query.filter_by(title=search).all()
            passed = 1
            anything_found = ''
        elif (s2 is not None):
            searched_user = s2.user_id
            events = Event.query.filter_by(user_id=searched_user).all()
            passed = 1
            anything_found = ''

    #if search filled and found with correct category
    elif (c1 is not None) and ((s1 is not None) or (s2 is not None)):
        if (s1 is not None):
            events = Event.query.filter_by(title=search, sport=category).all()
            passed = 1
            anything_found = ''
        elif (s2 is not None):
            searched_user = s2.user_id
            events = Event.query.filter_by(user_id=searched_user, sport=category).all()
            passed = 1
            anything_found = ''

    #if nothing can be found
    elif ((c1 is None) or (c1 is not None)) and (s1 is None) and (s2 is None):
        if search is not None:
            anything_found = 'Nothing was found matching those search terms'
            category = 'All'
            events = Event.query.all()
            passed = 1

    #if nothing above has been passed successfully then it definetly could not be found and can be assumed that the values haven't been
    # assigned yet or nothing at all could be found
    if passed == 0:
        if category is None:
            category = 'All'
            anything_found = ''
        else:
            anything_found = 'Nothing was found matching those search terms'
            category = 'All'
            events = Event.query.all()
            passed = 1

    return render_template('index.html', events=events, form=form, selected_category=category, anything_found=anything_found)


# serves images from uploads folder
# use 'url_for("download", filename=name)' in html to use this function
@bp.route('/uploads/<filename>')
@bp.route('/uploads')
def download(filename=None):
    if filename is not None:
        return send_from_directory(os.path.join(app.root_path, app.config["UPLOAD_FOLDER"]), filename)
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

        # join address information into a single entry
        addr = form.address.data

        status = form.status.data
        tickets_total = form.tickets_total.data
        price = form.price.data

        user_id = current_user.user_id

        new_event = Event(title=title, description=des, sport=sport, venue=venue, address=addr, 
            start_time=start_datetime, end_time=end_datetime, status=status, 
            tickets_total=tickets_total, price=price, user_id=user_id)
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
@login_required
def booked_events():
    orders = current_user.orders
    return render_template('booked_events.html', orders=orders)


@bp.route('/view-details/<event_id>', methods=['GET', 'POST'])
def view_details(event_id):
    event:Event = Event.query.filter_by(event_id=event_id).first()
    # if event cannot be found by query, raise a not found 404 exception
    if event is None:
        abort(404)


    set_current_event(event)
    cform = CommentForm()
    oform = OrderForm()
    oform.event_id = event_id
    if cform.validate_on_submit():
        text = cform.text.data
        user_id = current_user.user_id
        new_comment = Comment(text=text, user_id=user_id, event_id=event_id, date_of_creation=datetime.now())
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('main.view-details', event_id=event_id))

    if oform.is_submitted():
        if oform.validate():
            user_id = current_user.user_id
            ticket_quantity = oform.ticket_quantity.data
            new_order = Order(ticket_quantity=ticket_quantity, order_date=datetime.now(), user_id=user_id, event_id=event_id)
            db.session.add(new_order)
            db.session.commit()

            # if there are 0 remaing tickets, set status to booked
            if event.tickets_remaining == 0:
                event.status = BOOKED
                db.session.commit()
                
            return redirect(url_for('main.booked_events'))
        else:
            flash('Order attempt was unsuccessful')
    return render_template('view_details.html', event=event, oform=oform, cform=cform)


@bp.route('/delete-event/<event_id>')
@login_required
def delete_event(event_id):
    event:Event = Event.query.filter_by(event_id=event_id).first()
    if event is None:
        abort(404)

    if event.is_owner:
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('main.manage_events'))
    
    
@bp.route('/edit-event/<event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event:Event = Event.query.filter_by(event_id=event_id).first()
    if event is None:
        abort(404)


    set_current_event(event)

    if event is not None and event.is_owner:
        form = EventForm(obj=event)

        # set form mode to editing
        form.is_editing = True

        form.image.data = None
        
        if form.validate_on_submit():
            # populate event object with form data
            form.populate_event(event)

             # checks for image file and authenticates it
            image_file = form.image.data
            if (image_file and allowed_file(image_file.filename)):
                filename = secure_filename(image_file.filename)
                path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                image_file.save(path)
                event.image = filename

            db.session.commit()
            return redirect(url_for('main.manage_events'))
        
        form.start_time.data = event.start_time.time()
        form.start_date.data = event.start_time.date()
        form.end_time.data = event.end_time.time()
        form.end_date.data = event.end_time.date()

        form.address.data = event.address
        return render_template('create_event.html', form=form)


@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
