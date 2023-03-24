from . import database
from flask_login import UserMixin


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

    def __repr__(self) -> str:
        return f'''
        Voter (
            id: {self.id}
            roll_number_hash: {self.roll_number_hash}
            password: {self.password}
            wallet_address: {self.wallet_address}
            vote_status: {self.vote_status}
        )
        '''
