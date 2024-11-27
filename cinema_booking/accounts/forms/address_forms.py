from . import forms
from accounts.models.address_models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["billing_address", "city", "state", "zip_code"]
        widgets = {
            "billing_address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Billing Address", "id":"billing_address"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City", "id":"city"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "State", "id":"state"}
            ),
            "zip_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Zip Code", "id":"zip_code"}
            ),
        }