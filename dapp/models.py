from flask_login import UserMixin

from . import database


class Voter(database.Model, UserMixin):
    id = database.Column(
        database.Integer,
        primary_key=True
    )

    roll_number_hash = database.Column(
        database.String(64),
        unique=True
    )

    password = database.Column(
        database.String(88),
        nullable=False
    )

    wallet_address = database.Column(
        database.String(42),
        unique=True
    )

    vote_status = database.Column(
        database.Boolean,
        nullable=False,
        default=False
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
            roll_number_hash: {self.roll_number_hash}
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

    roll_number = database.Column(
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

    def __repr__(self) -> str:
        return f'''
            id: {self.id}
            roll_number: {self.roll_number}
            name: {self.name}
            vote_count: {self.vote_count}
        '''
