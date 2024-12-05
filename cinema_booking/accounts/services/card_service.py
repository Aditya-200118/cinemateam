# accounts/services/card_serivce.py

from accounts.repositories.card_repository import CardRepository
# all the business related logic goes here
from django.core.exceptions import ValidationError
from accounts.repositories.card_repository import CardRepository
from accounts.services.encryption_services import EncryptionService, FernetEncryptionStrategy
from accounts.services.validation_services import CardValidator

class CardService:
    def __init__(self, card_repository=None, encryption_service=None, validator=None):
        self.card_repository = card_repository or CardRepository()
        self.encryption_service = encryption_service or EncryptionService(FernetEncryptionStrategy())
        self.validator = validator or CardValidator()

    def add_card(self, customer, card_data):

        if self.card_repository.get_cards_by_customer(customer).count() >= 4:
            raise ValidationError("A customer can have a maximum of 4 cards.")
        # Validate card data
        self.validator.validate_card_number(card_data['card_number'])
        self.validator.validate_expiry_date(card_data['expiry_date'])
        self.validator.validate_cvv(card_data['cvv'])

        # Encrypt sensitive fields
        card_data['card_number'] = self.encryption_service.encrypt(card_data['card_number'])
        card_data['cvv'] = self.encryption_service.encrypt(card_data['cvv'])

        # Create the card
        return self.card_repository.create_card(customer, card_data)

    def get_customer_cards(self, customer):
        return self.card_repository.get_cards_by_customer(customer)

    def remove_card(self, card):
        self.card_repository.delete_card(card)

    def update_card(self, card, updated_data):
        if 'card_number' in updated_data:
            updated_data['card_number'] = self.encryption_service.encrypt(updated_data['card_number'])
        if 'cvv' in updated_data:
            updated_data['cvv'] = self.encryption_service.encrypt(updated_data['cvv'])

        return self.card_repository.update_card(card, updated_data)

    def decrypt_card_number(self, card_number):
        return self.encryption_service.decrypt(card_number)

    def decrypt_cvv(self, cvv):
        return self.encryption_service.decrypt(cvv)

    def decrypt_card_number_safe(self, card_number):
        decrypted_number = self.decrypt_card_number(card_number)
        return f"**** **** **** {decrypted_number[-4:]}"
    
    def decrypt_cvv_safe(self, cvv):
        decrypted_cvv = self.decrypt_cvv(cvv)
        return "*" * len(decrypted_cvv)

    def encrypt_card_data(self, card_number):
        return self.encryption_service.encrypt(card_number)
    
    def get_customer_card_count(self, customer):
        return self.card_repository.get_cards_by_customer(customer).count()
