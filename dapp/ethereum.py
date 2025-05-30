import json
import os

from datetime import datetime, timezone
from tzlocal import get_localzone
import pytz

from web3 import Web3

from .credentials import WEB3_PROVIDER_URL


class Blockchain:
    _ABI_DIR = f'{os.getcwd()}/contract/ABI.json'
    sepolia = 11155111

    def __init__(self, wallet_address, contract_address):
        self._read_ABI()
        self._wallet_address = wallet_address
        self._contract_address = contract_address

        self.w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
        self.w3.eth.default_account = self._wallet_address

        self._contract_instance = self.w3.eth.contract(
            abi=self._ABI,
            address=self._contract_address
        )


    def _read_ABI(self):
        with open(self._ABI_DIR) as ABI_file:
            self._ABI = json.loads(ABI_file.read())

    def _get_nonce(self):
        'Gets the nonce value form the wallet'
        return self.w3.eth.getTransactionCount(self._wallet_address)

    def local_to_utc_timestamp(self, local_timestamp: int) -> int:
        """
        Converts a local Unix timestamp (assumed to be in local timezone)
        to a UTC Unix timestamp.
        
        Args:
            local_timestamp (int): The timestamp in local time (seconds since epoch).
        
        Returns:
            int: Corresponding UTC timestamp (seconds since epoch).
        """
        # Get the system's local timezone (ZoneInfo object)
        local_tz = get_localzone()
        
        # Step 1: Create naive datetime from timestamp
        local_dt_naive = datetime.fromtimestamp(local_timestamp)
        
        # Step 2: Attach local timezone info using replace
        local_dt = local_dt_naive.replace(tzinfo=local_tz)
        
        # Step 3: Convert to UTC
        utc_dt = local_dt.astimezone(pytz.utc)
        
        # Step 4: Return UTC timestamp
        return int(utc_dt.timestamp())

    def set_voting_time(self, private_key, start_unix_time, end_unix_time):
        'Set election voting time in contract'
        print(" [set_voting_time] Building transaction...")

        start_unix_time_utc = self.local_to_utc_timestamp(start_unix_time)
        end_unix_time_utc = self.local_to_utc_timestamp(end_unix_time)

        print(f" [set_voting_time] start_unix_time: {start_unix_time_utc} {datetime.fromtimestamp(start_unix_time_utc).isoformat()}")


        try:
            tx = self._contract_instance.functions.setVotingTime(
                start_unix_time_utc,
                end_unix_time_utc
            ).buildTransaction(
                {
                    "gasPrice": self.w3.eth.gas_price,
                    "chainId": self.sepolia,
                    "from": self._wallet_address,
                    "nonce": self._get_nonce()
                }
            )

            # (Status, Tx msg)
            return (True, self._send_tx(tx, private_key))
        except Exception as e:
            return (False, str(e))

    def vote(self, private_key, candidate_hash, voter_hash):
        'Add a Vode hash in contract'
        candidate_hash = f'0x{candidate_hash}'
        voter_hash = f'0x{voter_hash}'

        print(" [vote] Building transaction...")

        try:
            tx = self._contract_instance.functions.vote(
                voter_hash,
                candidate_hash
            ).buildTransaction(
                {
                    "gasPrice": self.w3.eth.gas_price,
                    "gas": 2000000,
                    "chainId": self.sepolia,
                    "from": self._wallet_address,
                    "nonce": self._get_nonce()
                }
            )

            # (Status, Tx msg)
            return (True, self._send_tx(tx, private_key))
        except Exception as e:
            return (False, str(e))

    def extend_time(self, private_key, end_unix_time):
        'Extend the election time in contract'
        try:
            tx = self._contract_instance.functions.extendVotingTime(
                end_unix_time
            ).buildTransaction(
                {
                    "gasPrice": self.w3.eth.gas_price,
                    "chainId": self.sepolia,
                    "from": self._wallet_address,
                    "nonce": self._get_nonce()
                }
            )

            # (Status, Tx msg)
            return (True, self._send_tx(tx, private_key))
        except Exception as e:
            return (False, str(e))

    def _send_tx(self, tx, private_key):
        'Method for signing Tx and sending'
        private_key = f'0x{private_key}'

        print(" Signing Tx...")
        signed_tx = self.w3.eth.account.sign_transaction(
            tx,
            private_key=private_key
        )

        print(" Sending Tx...")
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        print(" Waiting for Tx receipt...")
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(
            tx_hash,
            timeout=180
        )

        print(tx_receipt['transactionHash'].hex())
        return tx_receipt['transactionHash'].hex()

    def get_hash_by_candidate_hash(self, candidate_hash):
        'Fetch the voting hash from the contract'
        candidate_hash = f'0x{candidate_hash}'

        vote_hash = self._contract_instance.functions.getCandidateVoteHash(
            candidate_hash
        ).call(
            {'from': self.w3.eth.defaultAccount}
        )

        return vote_hash.hex()

    def print_current_block_timestamp(self):
        timestamp = self._contract_instance.functions.getCurrentTimestamp().call()
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        print(f"Current contract block.timestamp: {timestamp} ({dt.isoformat()})")

    def fund_wallet(self, to_address):
        tx = {
            'to': to_address,
            'value': self.w3.toWei(0.002, 'ether'),
            'gas': 21000,
            'gasPrice': self.w3.eth.gas_price,
            "nonce": self._get_nonce(),
            'chainId': self.sepolia  # Sepolia
        }
        signed_tx = self.w3.eth.account.sign_transaction(tx, self._wallet_address)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

