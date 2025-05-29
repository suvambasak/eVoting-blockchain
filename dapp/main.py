from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from .db_operations import (add_new_vote_record, fetch_all_active_candidates,
                            fetch_candidate_by_id,
                            fetch_candidate_by_id_restricted,
                            fetch_contract_address, fetch_election,
                            fetch_election_result, fetch_voter_by_id,
                            fetch_voters_by_candidate_id)
from .ethereum import Blockchain
from .role import ElectionStatus
from .validator import build_vote_cast_hash, count_max_vote_owner_id, is_admin, sha256_hash
from .cryptography import encrypt_private_key, decrypt_private_key
from .models import Voter


main = Blueprint('main', __name__)


@main.route('/candidates')
@login_required
def candidates():
    'Shows the active candidate list and voter details'

    # Access deny for ADMIN
    if is_admin(current_user):
        return redirect(url_for('auth.index'))

    candidates = fetch_all_active_candidates()

    return render_template(
        'candidates.html',
        user=current_user,
        candidates=candidates
    )


@main.route('/cast_vote/<int:candidate_id>')
@login_required
def cast_vote(candidate_id):
    'When any vote button clicked'

    # Access deny for ADMIN
    if is_admin(current_user):
        return redirect(url_for('auth.index'))

    selected_candidate = fetch_candidate_by_id_restricted(candidate_id)
    private_key = decrypt_private_key(sha256_hash(current_user.username))

    # Get candidate and voter
    selected_candidate = fetch_candidate_by_id(candidate_id)
    voter = fetch_voter_by_id(current_user.id)

    # Generate hash
    candidate_hash, vote_hash = build_vote_cast_hash(
        selected_candidate,
        voter,
        fetch_voters_by_candidate_id(selected_candidate.id)
    )

    print(f'''
        candidate hash: {candidate_hash}
        vote_hash: {vote_hash}
    ''')

    # Sending transaction for vote cast
    blockchain = Blockchain(voter.wallet_address, fetch_contract_address())
    status, tx_msg = blockchain.vote(private_key, candidate_hash, vote_hash)

    if status:
        flash(f'Transaction confirmed: {tx_msg}')
        add_new_vote_record(voter, selected_candidate)
    else:
        flash(f'Transaction failed: {tx_msg}')



    return render_template(
        'candidates_confirm.html',
        selected_candidate=selected_candidate,
        private_key=private_key
    )


@main.route('/cast_vote/<int:candidate_id>/confirm', methods=['POST'])
@login_required
def cast_vote_confirm(candidate_id):
    '''
    Confirm the vote
    Take the private key of the voter to sign to transaction
    '''

    # Access deny for ADMIN
    if is_admin(current_user):
        return redirect(url_for('auth.index'))

    # Voter private key
    private_key = request.form.get('private_key').strip()

    # Get candidate and voter
    selected_candidate = fetch_candidate_by_id(candidate_id)
    voter = fetch_voter_by_id(current_user.id)

    # Generate hash
    candidate_hash, vote_hash = build_vote_cast_hash(
        selected_candidate,
        voter,
        fetch_voters_by_candidate_id(selected_candidate.id)
    )

    print(f'''
        candidate hash: {candidate_hash}
        vote_hash: {vote_hash}
    ''')

    # Sending transaction for vote cast
    blockchain = Blockchain(voter.wallet_address, fetch_contract_address())
    status, tx_msg = blockchain.vote(private_key, candidate_hash, vote_hash)

    if status:
        flash(f'Transaction confirmed: {tx_msg}')
        add_new_vote_record(voter, selected_candidate)
    else:
        flash(f'Transaction failed: {tx_msg}')

    return redirect(url_for('main.candidates'))


@main.route('/result')
def result():
    'Show the election result if published'

    # If not public
    election = fetch_election()
    if election.status == ElectionStatus.PRIVATE:
        flash('The result has not been released yet')
        return redirect(url_for('auth.index'))

    # Find the max vote count and IDs of the winners
    candidates = fetch_election_result()
    _, max_vote_owner_id = count_max_vote_owner_id(candidates)

    return render_template(
        'result.html',
        candidates=candidates,
        max_vote_owner_id=max_vote_owner_id
    )
