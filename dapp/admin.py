import time
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from .db_operations import (ban_candidate_by_id, ban_voter_by_id,
                            fetch_all_voters, fetch_election,
                            fetch_election_result,
                            fetch_voters_by_candidate_id, publish_result, fetch_contract_address, fetch_admin_wallet_address)
from .role import ElectionStatus
from .validator import (count_max_vote_owner_id, count_total_vote_cast,
                        is_admin, validate_result_hash)


from .ethereum import Blockchain

admin = Blueprint('admin', __name__)


@admin.route('/admin_panel')
@login_required
def admin_panel():
    'Shows the admin panel'

    # Access deny for other
    if not is_admin(current_user):
        return redirect(url_for('auth.index'))

    # Fetch all information
    election = fetch_election()
    voters = fetch_all_voters()
    candidates = fetch_election_result()

    # How many voted
    total_vote_cast = count_total_vote_cast(voters)
    # Max vote and IDs
    total_vote_count, max_vote_owner_id = count_max_vote_owner_id(candidates)

    return render_template(
        'admin_panel.html',
        election_status=election.status,
        candidates=candidates,
        max_vote_owner_id=max_vote_owner_id,
        voters=voters,
        total_voter=len(voters),
        total_vote_count=total_vote_count,
        total_vote_cast=total_vote_cast
    )


@admin.route('/publish')
@login_required
def publish():
    'Publish / Rollback election result'

    # Access deny for other
    if not is_admin(current_user):
        return redirect(url_for('auth.index'))

    candidates = fetch_election_result()
    for candidate in candidates:
        voters = fetch_voters_by_candidate_id(candidate.id)
        if candidate.vote_count != len(voters):
            return 'Error'

        print(validate_result_hash(voters, 'hash'))

    election = publish_result()

    # Notify current status
    if election.status == ElectionStatus.PUBLIC:
        flash('Election result is now public')
    else:
        flash('Election result is now private')

    return redirect(url_for('admin.admin_panel'))


@admin.route('/block_candidate/<int:candidate_id>')
@login_required
def block_candidate(candidate_id):
    'Block / Unblock candidate'

    # Access deny for other
    if not is_admin(current_user):
        return redirect(url_for('auth.index'))

    candidate = ban_candidate_by_id(candidate_id)
    flash(
        f"Candidate {candidate.name} ({candidate.username}) is {'Unblocked' if candidate.candidate_status else 'Blocked'}"
    )
    return redirect(url_for('admin.admin_panel'))


@admin.route('/block_voter/<int:voter_id>')
@login_required
def block_voter(voter_id):
    'Block / Unblock voter'

    # Access deny for other
    if not is_admin(current_user):
        return redirect(url_for('auth.index'))

    voter = ban_voter_by_id(voter_id)
    flash(
        f"Voter ({voter.username_hash}) is {'Unblocked' if voter.voter_status else 'Blocked'}"
    )
    return redirect(url_for('admin.admin_panel'))


@admin.route('/update_time', methods=['POST'])
@login_required
def update_time_post():
    'Extend the end time of the election'

    # Access deny for other
    if not is_admin(current_user):
        return redirect(url_for('auth.index'))

    # Get new time and private key input
    start_time = request.form.get('start_time').strip()
    end_time = request.form.get('end_time').strip()
    private_key = request.form.get('private_key').strip()

    if not private_key:
        flash('Private key empty')

    elif start_time and end_time:
        # Convert time to unix timestamp
        _start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        _end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
        unix_start_time = int(time.mktime(_start_time.timetuple()))
        unix_end_time = int(time.mktime(_end_time.timetuple()))

        print(start_time, unix_start_time)
        print(end_time, unix_end_time)
        print(private_key)

        contract_address = fetch_contract_address()
        print(contract_address)
        admin_wallet_address = fetch_admin_wallet_address()
        print(admin_wallet_address)

        # # TODO: Update the end time in smart contract
        # # Sign the Tx using the private key of ADMIN
        blockchain = Blockchain(admin_wallet_address, contract_address)
        status, tx_msg = blockchain.set_voting_time(
            private_key, unix_start_time, unix_end_time)

        if status:
            flash(f'[Updated] Tx HASH: {tx_msg}')
        else:
            flash(f'[Failed] Tx HASH: {tx_msg}')

    elif end_time:
        flash('Extend time not ready yet!')
        # flash(f'[Updated] Tx HASH: {tx_msg}')

    return redirect(url_for('admin.admin_panel'))
