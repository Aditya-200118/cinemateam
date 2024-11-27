from decimal import Decimal
from accounts.services.card_service import CardService
from accounts.repositories.transaction_repository import TransactionRepository


class TransactionService:
    def __init__(self, transaction_repository=None, card_service=None):
        self.transaction_repository = transaction_repository or TransactionRepository()
        self.card_service = card_service or CardService()

    def create_transaction(self, customer, booking, card_number, payment_amount):
        encrypted_card_number = self.card_service.encrypt_card_data(card_number)

        transaction = self.transaction_repository.create_transaction(
            customer=customer,
            payment_amount=payment_amount,
            encrypted_card_number=encrypted_card_number,
            booking_id=booking.booking_id,
        )
        return transaction