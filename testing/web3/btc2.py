from web3 import Web3


provider_url = "https://goerli.infura.io/v3/53be787bc8af4d34960ad23a2e7cebfb"
w3 = Web3(Web3.HTTPProvider(provider_url))
print(w3.isConnected())

# print(w3.eth.accounts[0])
print(w3.isAddress('0xf5D567f24d7e9a98687a5cd9b225792AFEFEbEB3'))

wallet = w3.toChecksumAddress('0xf5D567f24d7e9a98687a5cd9b225792AFEFEbEB3')
print(w3.eth.get_balance(wallet))
