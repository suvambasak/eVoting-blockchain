import hashlib

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import database
from .models import Voter
from .role import AccountStatus, UserRole, is_admin
from .validator import validate_signin, validate_signup

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')

    if is_admin(current_user):
        return redirect(url_for('admin.admin_panel'))

    return redirect(url_for('main.candidates'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signin', methods=['POST'])
def signin_post():
    roll_number = request.form.get('rollno').strip()
    password = request.form.get('pwd').strip()
    user_type = request.form['user_type']

    roll_number_hash = hashlib.sha256(
        bytes(roll_number, 'UTF-8')
    ).hexdigest()

    voter = Voter.query.filter_by(
        roll_number_hash=roll_number_hash
    ).first()

    if user_type == UserRole.VOTER:
        valid, msg = validate_signin(roll_number, password)
        if not valid:
            flash(msg)
            return redirect(url_for('auth.index'))

        if not voter:
            return redirect(url_for('auth.signup'))

        if not check_password_hash(voter.password, password):
            return redirect(url_for('auth.index'))

        if voter.voter_status == AccountStatus.BLOCKED:
            flash(f'{roll_number_hash} is blocked by ADMIN')
            return render_template('error.html', error_msg='BLOCKED')

        login_user(voter)
        return redirect(url_for('main.candidates'))

    elif user_type == UserRole.ADMIN:
        if check_password_hash(voter.password, password) and is_admin(voter):
            login_user(voter)
            return redirect(url_for('admin.admin_panel'))

    return render_template('error.html')


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
    confirm_password = request.form.get('cnf_pwd').strip()

    valid, msg = validate_signup(
        roll_number,
        wallet_address,
        password,
        confirm_password
    )

    if not valid:
        flash(msg)
        return redirect(url_for('auth.signup'))

    roll_number_hash = hashlib.sha256(bytes(roll_number, 'UTF-8')).hexdigest()
    password_hash = generate_password_hash(password, method='sha256')

    if Voter.query.filter_by(roll_number_hash=roll_number_hash).all():
        flash('Already registerd voter')
    else:
        database.session.add(
            Voter(
                roll_number_hash=roll_number_hash,
                password=password_hash,
                wallet_address=wallet_address,
                vote_status=False
            )
        )
        database.session.commit()

        flash('Voter registration complete')

    return redirect(url_for('auth.index'))
