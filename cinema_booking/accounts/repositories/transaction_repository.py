from accounts.models import Transaction

class TransactionRepository:
    @staticmethod
    def create_transaction(customer, payment_amount, encrypted_card_number, booking_id):
        # Generate a unique transaction ID (could use a UUID or any other unique logic)
        transaction_id = f"txn_{customer.pk}_{booking_id}_{int(payment_amount * 100)}"
        
        # Create and save the transaction
        transaction = Transaction.objects.create(
            transaction_id=transaction_id,
            customer=customer,
            encrypted_card_number = encrypted_card_number,
            payment_amount=payment_amount,
            booking_id=booking_id
        )
        return transaction
