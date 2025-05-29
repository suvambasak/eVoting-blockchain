from . import database
from .models import Candidate, Election, Otp, Voter
from .role import AccountStatus, UserRole

# Retrieve section


def fetch_contract_address():
    election = Election.query.filter_by(
        id=1
    ).first()
    return election.contract_address


def fetch_admin_wallet_address():
    admin = Voter.query.filter_by(
        id=UserRole.ADMIN_ID
    ).first()
    return admin.wallet_address


def fetch_election():
    return Election.query.filter_by(
        id=1
    ).first()


def fetch_voters_by_candidate_id(candidate_id):
    return Voter.query.filter_by(
        vote_status=candidate_id
    ).order_by(Voter.id).all()


def fetch_election_result():
    return Candidate.query.filter_by(
        candidate_status=AccountStatus.ACTIVE
    ).order_by(Candidate.vote_count.desc()).all()


def fetch_election_result_restricted():
    return Candidate.query.order_by(Candidate.vote_count.desc()).all()


def fetch_voter_by_username_hash(username_hash):
    return Voter.query.filter_by(
        username_hash=username_hash
    ).first()


def fetch_OTP_by_username_hash(username_hash):
    return Otp.query.filter_by(
        username_hash=username_hash
    ).first()


def fetch_all_voters():
    return Voter.query.filter(
        Voter.id > UserRole.ADMIN_ID
    ).all()


def fetch_candidate_by_id_restricted(candidate_id):
    return Candidate.query.with_entities(
        Candidate.id,
        Candidate.username,
        Candidate.name
    ).filter_by(
        id=candidate_id
    ).first()


def fetch_all_active_candidates():
    return Candidate.query.with_entities(
        Candidate.id,
        Candidate.username,
        Candidate.name
    ).filter(
        Candidate.candidate_status == AccountStatus.ACTIVE
    ).all()


def fetch_candidate_by_id(candidate_id):
    return Candidate.query.filter_by(
        id=candidate_id
    ).first()


def fetch_voter_by_id(voter_id):
    return Voter.query.filter_by(
        id=voter_id
    ).first()

# Block section


def ban_candidate_by_id(candidate_id):
    candidate = fetch_candidate_by_id(candidate_id)
    candidate.candidate_status = not candidate.candidate_status
    database.session.commit()
    return candidate


def ban_voter_by_id(voter_id):
    voter = fetch_voter_by_id(voter_id)
    voter.voter_status = not voter.voter_status
    database.session.commit()
    return voter

# Check section


def is_unverified_account(username_hash):
    if Otp.query.filter_by(
        username_hash=username_hash
    ).first():
        return True
    return False


def is_username_hash_already_exists(username_hash):
    if Voter.query.filter_by(
        username_hash=username_hash
    ).all():
        return True
    return False


def is_wallet_address_already_exists(wallet_address):
    if Voter.query.filter_by(
        wallet_address=wallet_address
    ).all():
        return True
    return False

# Add/Delete section


def add_new_vote_record(voter, candidate):
    voter.vote_status = candidate.id
    candidate.vote_count += 1
    database.session.commit()


def add_new_voter_signup(
        username_hash,
        password_hash,
        wallet_address,
        private_key_hash,
        otp
):
    database.session.add(
        Voter(
            username_hash=username_hash,
            password=password_hash,
            wallet_address=wallet_address,
            private_key_hash=private_key_hash,
            vote_status=False
        )
    )
    database.session.add(
        Otp(
            username_hash=username_hash,
            otp=otp
        )
    )
    database.session.commit()


def delete_OTP(otp):
    database.session.delete(otp)
    database.session.commit()


# Publish

def publish_result():
    election = Election.query.filter_by(
        id=1
    ).first()
    election.status = not election.status
    database.session.commit()
    return election
