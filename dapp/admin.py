from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import database
from .models import Candidate, Election, Voter
from .role import ElectionStatus, UserRole, is_admin

admin = Blueprint('admin', __name__)


@admin.route('/admin_panel')
@login_required
def admin_panel():
    if not is_admin(current_user):
        return redirect(url_for('auth.index'))

    election = Election.query.filter_by(
        id=1
    ).first_or_404()

    voters = Voter.query.filter(
        Voter.id > UserRole.ADMIN_ID
    ).all()

    candidates = Candidate.query.order_by(Candidate.vote_count.desc()).all()
    max_vote_owner_id = []
    if candidates:
        max_vote = candidates[0].vote_count

        for candidate in candidates:
            if candidate.vote_count == max_vote:
                max_vote_owner_id.append(candidate.id)

    return render_template(
        'admin_panel.html',
        election_status=election.status,
        candidates=candidates,
        max_vote_owner_id=max_vote_owner_id,
        voters=voters
    )


@admin.route('/publish')
@login_required
def publish():
    if not is_admin(current_user):
        return redirect(url_for('auth.index'))

    election = Election.query.filter_by(
        id=1
    ).first_or_404()
    election.status = not election.status
    database.session.commit()

    if election.status == ElectionStatus.PUBLIC:
        flash('Election result is now public')
    else:
        flash('Election result is now private')

    return redirect(url_for('admin.admin_panel'))


@admin.route('/block_candidate/<int:candidate_id>')
@login_required
def block_candidate(candidate_id):
    if not is_admin(current_user):
        return redirect(url_for('auth.index'))

    candidate = Candidate.query.filter_by(
        id=candidate_id
    ).first_or_404()

    candidate.candidate_status = not candidate.candidate_status
    database.session.commit()

    flash(
        f"Candidate {candidate.name} ({candidate.roll_number}) is {'Unblocked' if candidate.candidate_status else 'Blocked'}"
    )

    return redirect(url_for('admin.admin_panel'))


@admin.route('/block_voter/<int:voter_id>')
@login_required
def block_voter(voter_id):
    if not is_admin(current_user):
        return redirect(url_for('auth.index'))

    voter = Voter.query.filter_by(
        id=voter_id
    ).first_or_404()

    voter.voter_status = not voter.voter_status
    database.session.commit()

    flash(
        f"Voter ({voter.roll_number_hash}) is {'Unblocked' if voter.voter_status else 'Blocked'}"
    )

    return redirect(url_for('admin.admin_panel'))


@admin.route('/extend_time', methods=['POST'])
@login_required
def extend_time_post():
    if not is_admin(current_user):
        return redirect(url_for('auth.index'))

    new_time = request.form.get('new_time').strip()
    private_key = request.form.get('private_key').strip()

    print(new_time)
    print(private_key)

    return redirect(url_for('admin.admin_panel'))
