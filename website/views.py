from flask import Blueprint, render_template, url_for

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/create-event')
def create_event():
    return render_template('create_event.html')


@bp.route('/booked-events')
def booked_events():
    return render_template('booked_events.html')


@bp.route('/view-details')
def view_details():
    return render_template('view_details.html')
