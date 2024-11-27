# accounts/services/validation_service.py

import re
from django.core.exceptions import ValidationError
from django.utils import timezone

class CardValidator:
    def validate_card_number(self, card_number):
        if not re.match(r'^\d{16}$', card_number):
            raise ValidationError("Invalid card number format. It should be 16 digits.")

    def validate_expiry_date(self, expiry_date):
        if not re.match(r'^\d{2}/\d{2}$', expiry_date):
            raise ValidationError("Invalid expiry date format. Use MM/YY.")
        month, year = map(int, expiry_date.split('/'))
        current_year = timezone.now().year % 100
        current_month = timezone.now().month
        if year < current_year or (year == current_year and month < current_month):
            raise ValidationError("Expiry date cannot be in the past.")

    def validate_cvv(self, cvv):
        if not re.match(r'^\d{3,4}$', cvv):
            raise ValidationError("Invalid CVV format. It should be 3 or 4 digits.")
