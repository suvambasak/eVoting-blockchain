from flask_login import UserMixin

from . import database


class Otp(database.Model):
    id = database.Column(
        database.Integer,
        primary_key=True
    )

    username_hash = database.Column(
        database.String(64),
        unique=True,
        nullable=False
    )

    otp = database.Column(
        database.String(88),
        nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        OTPs (
            id: {self.id}
            username_hash: {self.username_hash}
            otp: {self.otp}
        )
        '''


class Voter(database.Model, UserMixin):
    id = database.Column(
        database.Integer,
        primary_key=True
    )

    username_hash = database.Column(
        database.String(64),
        unique=True,
        nullable=False
    )

    password = database.Column(
        database.String(88),
        nullable=False
    )

    wallet_address = database.Column(
        database.String(42),
        unique=True,
        nullable=False
    )

    private_key_encrypted = database.Column(
        database.String(88),
        nullable=False,
        unique=True
    )

    vote_status = database.Column(
        database.Integer,
        nullable=False,
        default=0
    )

    voter_status = database.Column(
        database.Boolean,
        nullable=False,
        default=True
    )

    def __repr__(self) -> str:
        return f'''
        Voter (
            id: {self.id}
            username_hash: {self.username_hash}
            password: {self.password}
            wallet_address: {self.wallet_address}
            vote_status: {self.vote_status}
            voter_status: {self.voter_status}
        )
        '''


class Candidate(database.Model):
    id = database.Column(
        database.Integer,
        primary_key=True
    )

    username = database.Column(
        database.String(64),
        unique=True
    )

    name = database.Column(
        database.String(100),
        nullable=False
    )

    vote_count = database.Column(
        database.Integer,
        default=0
    )

    candidate_status = database.Column(
        database.Boolean,
        nullable=False,
        default=True
    )

    def __repr__(self) -> str:
        return f'''
        Candidate(
            id: {self.id}
            username: {self.username}
            name: {self.name}
            vote_count: {self.vote_count}
            candidate_status: {self.candidate_status}
        )
        '''


class Election(database.Model):
    id = database.Column(
        database.Integer,
        primary_key=True
    )

    contract_address = database.Column(
        database.String(42),
        unique=True
    )

    status = database.Column(
        database.Boolean,
        nullable=False,
        default=False
    )

    def __repr__(self) -> str:
        return f'''
        Election(
            id: {self.id}
            contract_address: {self.contract_address}
            status: {self.status}
        )
        '''
