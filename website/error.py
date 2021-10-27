from werkzeug.exceptions import NotFound
from flask import Blueprint

er = Blueprint('error', __name__)

@er.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, NotFound):
        return e
