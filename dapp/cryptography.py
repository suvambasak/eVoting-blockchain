from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
# Load secret key
FERNET_KEY = os.environ.get("FERNET_KEY")
fernet = Fernet(FERNET_KEY)

# Encryption functions
def encrypt_private_key(private_key: str) -> str:
    return fernet.encrypt(private_key.encode()).decode()

def decrypt_private_key(encrypted_key: str) -> str:
    return fernet.decrypt(encrypted_key).decode()
