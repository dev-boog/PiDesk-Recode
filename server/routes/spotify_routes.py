from flask import Blueprint, render_template
from datetime import datetime

spotify_routes = Blueprint("spotify", __name__)

@spotify_routes.route('/spotify')
def spotify():
    return render_template('spotify.html')