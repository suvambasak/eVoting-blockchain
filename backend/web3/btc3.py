from web3 import Web3

provider_url = "https://goerli.infura.io/v3/53be787bc8af4d34960ad23a2e7cebfb"
w3 = Web3(Web3.HTTPProvider(provider_url))
# print(w3.isConnected())
# print(w3.isAddress('0xf5D567f24d7e9a98687a5cd9b225792AFEFEbEB3'))


abi = '''[
	{
		"inputs": [],
		"name": "dec",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "inc",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "count",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "get",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]'''
contract_addr = '0x68220CD48B53DfB831885fC59bC0D605628fDFC3'
contract_ins = w3.eth.contract(address=contract_addr, abi=abi)

wallet = w3.toChecksumAddress('0xf5D567f24d7e9a98687a5cd9b225792AFEFEbEB3')
nonce = w3.eth.get_transaction_count(wallet)
print(nonce)
goerli = 5

tx_build = contract_ins.functions.inc().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": goerli,
        "from": wallet,
        "nonce": nonce
    }
)
# print(tx_build)


private_key = '0x7ca8bda434135489bf254303430fd1411e92bbe48ceaabfebe840f9672ee1e19'
tx_signed = w3.eth.account.sign_transaction(tx_build, private_key)

tx_hash = w3.eth.send_raw_transaction(tx_signed.rawTransaction)

tx_recp = w3.eth.wait_for_transaction_receipt(tx_hash)

print(tx_recp)
