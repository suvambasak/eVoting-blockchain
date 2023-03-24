from flask import Blueprint, render_template, url_for, request, redirect

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    return render_template('index.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signin', methods=['POST'])
def signin_post():
    roll_number = request.form.get('rollno')
    password = request.form.get('pwd')

    print(roll_number, password)

    return redirect(url_for('main.candidates'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    roll_number = request.form.get('rollno')
    wallet_address = request.form.get('walletaddr')
    password = request.form.get('pwd')

    print(roll_number, wallet_address, password)

    return redirect(url_for('auth.index'))
