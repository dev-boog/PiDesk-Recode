from flask import Blueprint, render_template
from datetime import datetime

error_routes = Blueprint("error", __name__)

@error_routes.route('/error')
def error():
    return render_template('error.html', error_title="", error_description="", redirect="")