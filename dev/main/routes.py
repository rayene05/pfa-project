from flask import render_template
from flask import Blueprint
from flask_login import login_required
main=Blueprint('main',__name__)
@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')
@main.route('/learnmore')
def learnmore():
    return render_template('learnmore.html')
