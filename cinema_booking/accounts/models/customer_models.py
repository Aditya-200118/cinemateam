#  accounts/models/customer_models.py

from . import models
from accounts.models.user_models import User 

class Customer(User):
    address = models.OneToOneField(
        "Address", on_delete=models.CASCADE, related_name="customer"
    )
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    promotions = models.BooleanField(default=False)