from web3 import Web3
WEB3_PROVIDER_URL = "https://goerli.infura.io/v3/53be787bc8af4d34960ad23a2e7cebfb"


def validate_signin(roll_number, password):
    if len(roll_number) < 5 or not roll_number.isdigit():
        return (False, 'Invalid roll number')

    if not password:
        return (False, 'Invalid password')

    return (True, '')


def validate_signup(
        roll_number,
        wallet_address,
        password,
        confirm_password
):
    if len(roll_number) < 5 or not roll_number.isdigit():
        return (False, 'Invalid roll number')

    w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
    if len(wallet_address) != 42 or not w3.isAddress(wallet_address):
        return (False, 'Invalid wallet address')

    if not password:
        return (False, 'Invalid password')
    if confirm_password != password:
        return (False, 'Confirm password does not match')

    return (True, '')
