import getpass
import json
import sys

import solcx
from solcx import compile_standard
from web3 import Web3

from dapp.credentials import WEB3_PROVIDER_URL

solcx.install_solc('0.8.19')
w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
sepolia = 11155111

# Input private key
private_key = getpass.getpass(prompt='Private key: ')
private_key = '0x'+private_key

sys.stdout.write(f'\r Reading admin details...          ')
with open('admin/admin.json') as json_file:
    admin_details = json.loads(json_file.read())
    admin_wallet = admin_details['wallet']
sys.stdout.write(f'\r Reading contract...               ')
with open('contract/mysol2.sol', 'r') as contract_file:
    contract = contract_file.read()


# Compile
sys.stdout.write(f'\r Compiling contract...               ')
compiled_solidity = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "evote.sol": {
                    "content": contract
            }
        },
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        }
    },
    solc_version="0.8.19"
)
ABI = compiled_solidity['contracts']['evote.sol']['EVoting']['abi']
BYTECODE = compiled_solidity['contracts']['evote.sol']['EVoting']['evm']['bytecode']['object']

# Deployment
contract_instance = w3.eth.contract(abi=ABI, bytecode=BYTECODE)
nonce = w3.eth.getTransactionCount(admin_wallet)

sys.stdout.write(f'\r Building transaction...               ')
tx = contract_instance.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": sepolia,
        "from": admin_wallet,
        "nonce": nonce
    }
)
sys.stdout.write(f'\r Signing transaction...               ')
signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
sys.stdout.write(f'\r Waiting for Tx receipt...             ')
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


admin_details['contract_address'] = tx_receipt.contractAddress
print(f'\n contract_address: {tx_receipt.contractAddress}')


# Writing ABI and contract address
with open('contract/ABI.json', 'w') as ABI_file:
    ABI_file.write(json.dumps(ABI))

with open('admin/admin.json', 'w') as json_file:
    json_file.write(json.dumps(admin_details, indent=4))
