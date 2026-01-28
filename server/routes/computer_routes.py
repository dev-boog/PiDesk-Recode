from flask import Blueprint, render_template

computer_routes = Blueprint("computer", __name__)

@computer_routes.route('/computer')
def computer():
    return render_template('computer.html')