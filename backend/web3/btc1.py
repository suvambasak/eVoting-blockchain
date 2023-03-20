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
token_get = contract_ins.functions.get().call()
print(token_get)
