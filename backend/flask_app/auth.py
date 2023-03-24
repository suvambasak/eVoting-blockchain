from flask import Blueprint, render_template, url_for

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    return render_template('index.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')
