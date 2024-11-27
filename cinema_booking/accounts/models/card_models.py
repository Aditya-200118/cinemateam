# accounts/models/card_models.py

from . import models, ValidationError, Fernet, settings, logging
from accounts.models.customer_models import Customer
logger = logging.getLogger(__name__)

class Card(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="cards"
    )
    card_name = models.CharField(max_length=100, default="")
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)

class Transaction(models.Model):
   
    transaction_id = models.CharField(max_length=255, unique=True)
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="transactions")
    
    encrypted_card_number = models.CharField(max_length=255)
    
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    booking_id = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=50, default="pending")

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.payment_amount} by {self.customer}"

    class Meta:
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['customer']),
            models.Index(fields=['created_at']),
        ]
