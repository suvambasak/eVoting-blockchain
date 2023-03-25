from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Voter
from . import database
import hashlib

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.candidates'))
    return render_template('index.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signin', methods=['POST'])
def signin_post():
    roll_number = request.form.get('rollno').strip()
    password = request.form.get('pwd').strip()

    roll_number_hash = hashlib.sha256(bytes(roll_number, 'UTF-8')).hexdigest()

    voter = Voter.query.filter_by(roll_number_hash=roll_number_hash).first()

    if not voter:
        return redirect(url_for('auth.signup'))

    if not check_password_hash(voter.password, password):
        return redirect(url_for('auth.index'))

    # Login code here
    login_user(voter)

    return redirect(url_for('main.candidates'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    roll_number = request.form.get('rollno').strip()
    wallet_address = request.form.get('walletaddr').strip()
    password = request.form.get('pwd').strip()

    roll_number_hash = hashlib.sha256(bytes(roll_number, 'UTF-8')).hexdigest()
    password_hash = generate_password_hash(password, method='sha256')

    # print(roll_number, roll_number_hash, len(roll_number_hash))
    # print(wallet_address)
    # print(password, password_hash, len(password_hash))

    if not Voter.query.filter_by(roll_number_hash=roll_number_hash).all():
        database.session.add(
            Voter(
                roll_number_hash=roll_number_hash,
                password=password_hash,
                wallet_address=wallet_address,
                vote_status=False
            )
        )
        database.session.commit()

    return redirect(url_for('auth.index'))
