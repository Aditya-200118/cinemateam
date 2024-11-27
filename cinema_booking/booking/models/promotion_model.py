# booking/models/promotion_model.py

from . import *

# booking/promotion_models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Promotion(models.Model):
    promo_code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=100, default="N/A")
    description = models.TextField(default="N/A") 
    discount = models.FloatField()
    valid_from = models.DateField(default=timezone.now)
    valid_to = models.DateField(default=timezone.now().date() + timedelta(days=30)) 

    def add_promotion(self, promo_code, title, description, discount, valid_from, valid_to):
        promotion = Promotion(
            promo_code=promo_code,
            title=title,
            description=description,
            discount=discount,
            valid_from=valid_from or timezone.now().date(),
            valid_to=valid_to or (timezone.now().date() + timedelta(days=30))
        )
        promotion.save()
        return promotion

    def remove_promotion(self):
        """Delete the promotion instance."""
        self.delete()

    def __str__(self):
        return self.promo_code
    

class CouponUsage(models.Model):
    customer = models.ForeignKey(
        'accounts.Customer', on_delete=models.CASCADE, related_name='coupon_usages'
    )
    promotion = models.ForeignKey(
        Promotion, on_delete=models.CASCADE, related_name='usages'
    )
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'promotion')  # Ensures one-time use per customer

    def __str__(self):
        return f"{self.customer.email} - {self.promotion.promo_code}"