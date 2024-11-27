# accounts/services/card_facade.py

from accounts.services.card_service import CardService
import logging
logger = logging.getLogger(__name__)

class CardFacade:
    def __init__(self):
        self.card_service = CardService()

    def add_card(self, customer, card_data):
        """
        Add a new card, encrypt card number and CVV.
        """
        return self.card_service.add_card(customer, card_data)

    def update_card(self, card, updated_data):
        """
        Update an existing card, ensuring encryption of card number and CVV if modified.
        """
        return self.card_service.update_card(card, updated_data)

    def delete_card(self, card):
        """
        Delete a payment method card securely.
        """
        self.card_service.remove_card(card)

    def decrypt_card_number(self, card_number):
        """
        Decrypt the card number.
        """
        return self.card_service.decrypt_card_number(card_number)

    def decrypt_cvv(self, cvv):
        """
        Decrypt the CVV.
        """
        return self.card_service.decrypt_cvv(cvv)

    def decrypt_card_number_safe(self, card_number):
        """
        Decrypt card number and mask it, showing only last 4 digits.
        """
        return self.card_service.decrypt_card_number_safe(card_number)
    
    def decrypt_cvv_safe(self, cvv):
        """
        Decrypt CVV and mask it with stars.
        """
        return self.card_service.decrypt_cvv_safe(cvv)