from flask import session
from .models import Event

def set_current_event(event:Event):
    session['current_event'] = event.event_id

def get_current_event() -> Event:
    return Event.query.filter_by(event_id=session['current_event']).first()