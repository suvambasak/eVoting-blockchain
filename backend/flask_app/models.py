from . import database


class Voter(database.Model):
    roll_number_hash = database.Column(
        database.String(64),
        primary_key=True
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
            roll_number_hash: {self.roll_number_hash}
            password: {self.password}
            wallet_address: {self.wallet_address}
            vote_status: {self.vote_status}
        )
        '''
