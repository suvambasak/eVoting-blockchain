from .credentials import WEB3_PROVIDER_URL
from web3 import Web3
import os
import json


class Blockchain:
    _ABI_DIR = f'{os.getcwd()}/contract/ABI.json'
    sepolia = 11155111

    def __init__(self, wallet_address, contract_address):
        self._read_ABI()
        self._wallet_address = wallet_address
        self._contract_address = contract_address

        self.w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))

        self._contract_instance = self.w3.eth.contract(
            abi=self._ABI,
            address=self._contract_address
        )

    def _read_ABI(self):
        with open(self._ABI_DIR) as ABI_file:
            self._ABI = json.loads(ABI_file.read())

    def _get_nonce(self):
        return self.w3.eth.getTransactionCount(self._wallet_address)

    def set_voting_time(self, private_key, start_unix_time, end_unix_time):
        print(" [set_voting_time] Building transaction...")

        try:
            tx = self._contract_instance.functions.setVotingTime(
                start_unix_time,
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

    def vote(self, private_key, candidate_hash, voter_hash):
        candidate_hash = f'0x{candidate_hash}'
        voter_hash = f'0x{voter_hash}'

        try:
            tx = self._contract_instance.functions.vote(
                voter_hash,
                candidate_hash
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
        candidate_hash = f'0x{candidate_hash}'
        print(candidate_hash)
        token_get = self._contract_instance.functions.getCandidateVoteCount(
            candidate_hash).send()
        print(token_get.hex())
