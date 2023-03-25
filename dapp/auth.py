import hashlib

from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import database
from .models import Candidate, Voter

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

    flash('Voter registration complete')
    return redirect(url_for('auth.index'))


@auth.route('/result')
def result():
    candidates = Candidate.query.order_by(Candidate.vote_count.desc()).all()
    max_vote_owner_id = []
    if candidates:
        max_vote = candidates[0].vote_count

        for candidate in candidates:
            if candidate.vote_count == max_vote:
                max_vote_owner_id.append(candidate.id)

    return render_template('result.html', candidates=candidates, max_vote_owner_id=max_vote_owner_id)
