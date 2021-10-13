from flask import Blueprint, render_template, url_for, session, request
from flask_login import login_required

from website.forms import EventForm, TestForm

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.is_submitted():
        print(request.form) # just for testing purposes
    return render_template('create_event.html')

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
