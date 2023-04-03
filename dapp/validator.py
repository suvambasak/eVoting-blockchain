import hashlib
import random
import string

from web3 import Web3

from .credentials import WEB3_PROVIDER_URL
from .role import UserRole


def is_admin(user):
    if user.id == UserRole.ADMIN_ID:
        return True
    return False


def validate_signin(username, password):
    if len(username) < 3:
        return (False, 'Invalid username')

    if not password:
        return (False, 'Invalid password')

    return (True, '')


def validate_signup(
        username,
        wallet_address,
        password,
        confirm_password
):
    if len(username) < 3:
        return (False, 'Invalid username')

    w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
    if len(wallet_address) != 42 or not w3.isAddress(wallet_address):
        return (False, 'Invalid wallet address')

    if not password:
        return (False, 'Invalid password')
    if confirm_password != password:
        return (False, 'Confirm password does not match')

    return (True, '')


def generate_opt(length):
    otp = ''
    for _ in range(length):
        otp += random.choice(string.digits)
    return otp


def sha256_hash(username):
    return hashlib.sha256(
        bytes(username, 'UTF-8')
    ).hexdigest()


def count_total_vote_cast(voters):
    total_vote_cast = 0
    for voter in voters:
        if voter.vote_status:
            total_vote_cast += 1
    return total_vote_cast


def count_max_vote_owner_id(candidates):
    max_vote_owner_id = []
    total_vote_count = 0
    if candidates:
        max_vote = candidates[0].vote_count

        for candidate in candidates:
            total_vote_count += candidate.vote_count
            if candidate.vote_count == max_vote:
                max_vote_owner_id.append(candidate.id)

    return (total_vote_count, max_vote_owner_id)
