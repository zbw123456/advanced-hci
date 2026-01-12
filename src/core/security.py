"""
Security Manager for Data Encryption.
Uses AES encryption (via Fernet) to secure local data.
"""
from cryptography.fernet import Fernet
import os

class SecurityManager:
    def __init__(self, key_path="secret.key"):
        self.key_path = key_path
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)

    def _load_or_generate_key(self):
        """Load existing key or generate a new one."""
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as key_file:
                key_file.write(key)
            return key

    def encrypt(self, data: str) -> bytes:
        """Encrypt a string."""
        return self.cipher.encrypt(data.encode())

    def decrypt(self, token: bytes) -> str:
        """Decrypt a token back to string."""
        return self.cipher.decrypt(token).decode()
