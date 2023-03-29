from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required

from . import database
from .models import Candidate, Voter

main = Blueprint('main', __name__)


@main.route('/candidates')
@login_required
def candidates():
    candidates = Candidate.query.with_entities(
        Candidate.id,
        Candidate.roll_number,
        Candidate.name
    ).all()
    return render_template('candidates.html', user=current_user, candidates=candidates)


@main.route('/cast_vote/<int:candidate_id>')
@login_required
def cast_vote(candidate_id):
    selected_candidate = Candidate.query.with_entities(
        Candidate.id,
        Candidate.roll_number,
        Candidate.name
    ).filter_by(
        id=candidate_id
    ).first_or_404()

    return render_template('candidates_confirm.html', selected_candidate=selected_candidate)


@main.route('/cast_vote/<int:candidate_id>/confirm', methods=['POST'])
@login_required
def cast_vote_confirm(candidate_id):
    flash('Processing')

    parivate_key = request.form.get('parivate_key').strip()

    selected_candidate = Candidate.query.filter_by(
        id=candidate_id
    ).first_or_404()

    voter = Voter.query.filter_by(
        id=current_user.id
    ).first_or_404()

    voter.vote_status = True
    selected_candidate.vote_count += 1
    database.session.commit()

    flash('Transaction confirmed')
    return redirect(url_for('main.candidates'))


@main.route('/result')
def result():
    candidates = Candidate.query.order_by(Candidate.vote_count.desc()).all()
    max_vote_owner_id = []
    if candidates:
        max_vote = candidates[0].vote_count

        for candidate in candidates:
            if candidate.vote_count == max_vote:
                max_vote_owner_id.append(candidate.id)

    return render_template('result.html', candidates=candidates, max_vote_owner_id=max_vote_owner_id)
