from flask import render_template
from werkzeug.exceptions import NotFound
from flask import Blueprint

er = Blueprint('error', __name__)

@er.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@er.errorhandler(500)
def not_found_error(error):
    return render_template('500.html'), 500

