from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .credentials import EMAIL_SERVICE
from .db_operations import (add_new_voter_signup, delete_OTP,
                            fetch_OTP_by_username_hash,
                            fetch_voter_by_username_hash,
                            is_unverified_account,
                            is_username_hash_already_exists,
                            is_wallet_address_already_exists)
from .mail_server import MailServer
from .role import AccountStatus
from .validator import (generate_opt, is_admin, sha256_hash, validate_signin,
                        validate_signup)

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    '''
    Show login page
    If Admin session found redirect to admin panel
    If Voter session found redirect to candidate page
    '''

    if not current_user.is_authenticated:
        return render_template('index.html')

    if is_admin(current_user):
        return redirect(url_for('admin.admin_panel'))

    return redirect(url_for('main.candidates'))


@auth.route('/signup')
def signup():
    'Show signup page'
    return render_template('signup.html')


@auth.route('/signin', methods=['POST'])
def signin_post():
    'Login POST request for Voters and Admin'

    # Get the input credentials
    username = request.form.get('username').strip()
    password = request.form.get('pwd').strip()
    # Username HASH
    username_hash = sha256_hash(username)

    # Validate the inputs
    valid, msg = validate_signin(username, password)
    if not valid:
        flash(msg)
        return redirect(url_for('auth.index'))

    # Get the voter details
    voter = fetch_voter_by_username_hash(username_hash)

    # If voter not found in DB
    if not voter:
        flash('User not found!')
        return redirect(url_for('auth.signup'))

    # If OTP is not verified
    if is_unverified_account(username_hash):
        return render_template('otp.html', username_hash=username_hash)

    # Input password check
    if not check_password_hash(voter.password, password):
        flash('Incorrect password')
        return redirect(url_for('auth.index'))

    # If the user is ADMIN
    if is_admin(voter):
        login_user(voter)  # login session
        return redirect(url_for('admin.admin_panel'))

    # If the user blocked
    if voter.voter_status == AccountStatus.BLOCKED:
        flash(f'{username_hash} is blocked by ADMIN')
        return render_template('error.html', error_msg='BLOCKED')

    # Start login session
    login_user(voter)
    return redirect(url_for('main.candidates'))


@auth.route('/logout')
@login_required
def logout():
    'Logout the user'
    logout_user()
    return redirect(url_for('auth.index'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    'Signup POST request for voters'

    # Get input details
    username = request.form.get('username').strip()
    wallet_address = request.form.get('walletaddr').strip()
    password = request.form.get('pwd').strip()
    confirm_password = request.form.get('cnf_pwd').strip()

    # Create hashs
    username_hash = sha256_hash(username)
    password_hash = generate_password_hash(password, method='sha256')

    # Validate inputs
    valid, msg = validate_signup(
        username,
        wallet_address,
        password,
        confirm_password
    )
    if not valid:
        flash(msg)
        return redirect(url_for('auth.signup'))

    # If duplicate username
    if is_username_hash_already_exists(username_hash):
        flash('Already registerd voter')
        return redirect(url_for('auth.index'))

    # If duplicate wallet address
    elif is_wallet_address_already_exists(wallet_address):
        flash('Incorrect wallet address')
        return redirect(url_for('auth.signup'))

    # New voter adding
    else:
        otp = generate_opt(6)
        print(f'OTP: {otp}')

        if EMAIL_SERVICE:
            mail_agent = MailServer()
            email, _ = mail_agent.send_mail(username, otp)
            flash(f'Enter the code sent to {email}')

        add_new_voter_signup(
            username_hash,
            password_hash,
            wallet_address,
            generate_password_hash(otp, method='sha256')
        )

        return render_template('otp.html', username_hash=username_hash)


@auth.route('/verify_otp/<string:username_hash>', methods=['POST'])
def verify_otp_post(username_hash):
    'OTP verification POST request'

    # Get input OTP
    user_otp = request.form.get('otp').strip()

    otp = fetch_OTP_by_username_hash(username_hash)

    # If not such OTP exist
    if not otp:
        return redirect(url_for('auth.index'))

    # OTP match
    if check_password_hash(otp.otp, user_otp):
        delete_OTP(otp)

        flash('Voter registration complete')
        return redirect(url_for('auth.index'))

    flash('Incorrect OTP')
    return render_template('otp.html', username_hash=username_hash)
