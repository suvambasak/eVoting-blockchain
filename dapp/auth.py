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
    username = request.form.get('username').strip()
    password = request.form.get('pwd').strip()

    valid, msg = validate_signin(username, password)
    if not valid:
        flash(msg)
        return redirect(url_for('auth.index'))

    username_hash = hashlib.sha256(
        bytes(username, 'UTF-8')
    ).hexdigest()
    voter = Voter.query.filter_by(
        username_hash=username_hash
    ).first()

    if not voter:
        flash('User not found!')
        return redirect(url_for('auth.signup'))

    if not check_password_hash(voter.password, password):
        flash('Incorrect password')
        return redirect(url_for('auth.index'))

    if is_admin(voter):
        login_user(voter)
        return redirect(url_for('admin.admin_panel'))

    if voter.voter_status == AccountStatus.BLOCKED:
        flash(f'{username_hash} is blocked by ADMIN')
        return render_template('error.html', error_msg='BLOCKED')

    login_user(voter)
    return redirect(url_for('main.candidates'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username').strip()
    wallet_address = request.form.get('walletaddr').strip()
    password = request.form.get('pwd').strip()
    confirm_password = request.form.get('cnf_pwd').strip()

    valid, msg = validate_signup(
        username,
        wallet_address,
        password,
        confirm_password
    )
    if not valid:
        flash(msg)
        return redirect(url_for('auth.signup'))

    if Voter.query.filter_by(wallet_address=wallet_address).all():
        flash('Incorrect wallet address')
        return redirect(url_for('auth.signup'))

    username_hash = hashlib.sha256(bytes(username, 'UTF-8')).hexdigest()
    password_hash = generate_password_hash(password, method='sha256')

    if Voter.query.filter_by(username_hash=username_hash).all():
        flash('Already registerd voter')
    else:
        database.session.add(
            Voter(
                username_hash=username_hash,
                password=password_hash,
                wallet_address=wallet_address,
                vote_status=False
            )
        )
        database.session.commit()

        flash('Voter registration complete')

    return redirect(url_for('auth.index'))
