# accounts/services/card_facade.py

from accounts.services.card_service import CardService
import logging
logger = logging.getLogger(__name__)
from accounts.repositories.card_repository import CardRepository
from django.core.exceptions import ValidationError
from accounts.services.encryption_services import EncryptionService, FernetEncryptionStrategy
from accounts.services.validation_services import CardValidator

class CardFacade:
    def __init__(self):
        self.card_service = CardService()

    def add_card(self, customer, card_data):
        return self.card_service.add_card(customer, card_data)

    def update_card(self, card, updated_data):
        return self.card_service.update_card(card, updated_data)

    def delete_card(self, card):
        self.card_service.remove_card(card)

    def decrypt_card_number(self, card_number):
        return self.card_service.decrypt_card_number(card_number)

    def decrypt_cvv(self, cvv):
        return self.card_service.decrypt_cvv(cvv)

    def decrypt_card_number_safe(self, card_number):
        return self.card_service.decrypt_card_number_safe(card_number)
    
    def decrypt_cvv_safe(self, cvv):
        return self.card_service.decrypt_cvv_safe(cvv)

    def get_customer_card_count(self, customer):
        return self.card_service.get_customer_card_count(customer)