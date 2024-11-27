# forms/card_form.py
from accounts.models import Card
from . import *
import re
from django.core.exceptions import ValidationError
from django.utils import timezone

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["card_name", "card_number", "expiry_date", "cvv"]
        widgets = {
            'card_number': forms.TextInput(attrs={'placeholder': 'Card Number', 'class': 'form-control', 'id':'card_number'}),
            'card_name': forms.TextInput(attrs={'placeholder': 'Name on Card', 'class': 'form-control', 'id': 'card_name'}),
            'expiry_date': forms.TextInput(attrs={'placeholder': 'MM/YY', 'class': 'form-control', 'id': 'card_date'}),
            'cvv': forms.PasswordInput(attrs={'placeholder': 'CVV', 'class': 'form-control', 'id': 'card_cvv'}),
        }

    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop("customer", None)
        self.is_registration = kwargs.pop("is_registration", False)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not self.is_registration and self.customer and self.customer.cards.count() >= 4:
            raise ValidationError('A customer can only have up to four payment methods.')
        return cleaned_data

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not re.match(r'^\d{14,16}$', card_number):
            raise ValidationError("Invalid card number format. It should be 14, 15, or 16 digits.")
        return card_number

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if not re.match(r'^\d{2}/\d{2}$', expiry_date):
            raise ValidationError("Invalid expiry date format. Use MM/YY.")
        month, year = map(int, expiry_date.split('/'))
        if month < 1 or month > 12:
            raise ValidationError("Invalid expiry month.")
        current_year = timezone.now().year % 100
        current_month = timezone.now().month
        if year < current_year or (year == current_year and month < current_month):
            raise ValidationError("Expiry date cannot be in the past.")
        return expiry_date

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if not re.match(r'^\d{3,4}$', cvv):
            raise ValidationError("Invalid CVV format. It should be 3 or 4 digits.")
        return cvv


class ModifyCardForm(CardForm):
    delete = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        super().__init__(*args, **kwargs)
        self.fields['delete'] = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())

        self.initial = initial

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('delete'):
            return cleaned_data  # Skip further validation if deleting
        return cleaned_data