# accounts/services/encryption_service.py

from cryptography.fernet import Fernet
from django.conf import settings

class EncryptionStrategy:
    def encrypt(self, data):
        raise NotImplementedError

    def decrypt(self, data):
        raise NotImplementedError

class FernetEncryptionStrategy(EncryptionStrategy):
    def __init__(self):
        self.fernet = Fernet(settings.ENCRYPTION_KEY)

    def encrypt(self, data):
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, data):
        return self.fernet.decrypt(data.encode()).decode()

class EncryptionService:
    def __init__(self, strategy: FernetEncryptionStrategy):
        self.strategy = strategy

    def encrypt(self, data):
        return self.strategy.encrypt(data)

    def decrypt(self, data):
        return self.strategy.decrypt(data)