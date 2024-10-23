from django import forms
from django.contrib.auth import get_user_model
from .models import Card, Address
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"placeholder": "Email address", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        ),
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label="Remember Me"
    )


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control", "id": "password"}
        ),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                message="Password must be at least 8 characters long, contain letters, numbers, and at least one special character."
            )
        ]
    )

    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat password",
                "class": "form-control",
                "id": "password2",
            }
        ),
    )
    
    promotions = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        label="I want to receive promotions and updates"
    )

    class Meta:
        model = get_user_model()
        fields = ["first_name", "middle_name", "last_name", "contact_no", "email", "promotions"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First Name",
                    "required": True,
                }
            ),
            "middle_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Middle Name"}
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last Name",
                    "required": True,
                }
            ),
            "contact_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Contact Number",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email",
                    "id": "email",
                    "required": True,
                    "pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                    "title": "Please enter a valid email address.",
                }
            ),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        password = cd.get("password")
        password2 = cd.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def clean_email(self):
        data = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already in use.")
        return data



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["billing_address", "city", "state", "zip_code"]
        widgets = {
            "billing_address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Billing Address"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "State"}
            ),
            "zip_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Zip Code"}
            ),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if self.instance.pk and hasattr(self.instance, 'customer'):
    #         raise forms.ValidationError('A customer can only have one address.')


from django import forms
from .models import Card
from django.core.exceptions import ValidationError
import re
from django.utils import timezone

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["card_number", "expiry_date", "cvv"]
        widgets = {
            'card_number': forms.TextInput(attrs={'placeholder': 'Card Number', 'class': 'form-control'}),
            'expiry_date': forms.TextInput(attrs={'placeholder': 'MM/YY', 'class': 'form-control'}),
            'cvv': forms.PasswordInput(attrs={'placeholder': 'CVV', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.is_registration = kwargs.pop("is_registration", False)
        super().__init__(*args, **kwargs)

    # def clean_card_number(self):
    #     card_number = self.cleaned_data.get('card_number')
    #     if not re.match(r'^\d{16}$', card_number):
    #         raise ValidationError("Invalid card number format. It should be 16 digits.")
    #     return card_number

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

    def clean(self):
        cleaned_data = super().clean()
        if not self.is_registration:
            customer = self.instance.customer
            if not customer:
                raise ValidationError("The card must be associated with a customer.")
            if customer.cards.count() >= 4:
                raise ValidationError("You cannot store more than 4 payment cards.")
        return cleaned_data




# from .models import Customer
from django import forms
from django.contrib.auth import get_user_model

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "contact_no", "promotions"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "contact_no": forms.TextInput(attrs={"class": "form-control", "placeholder": "Contact Number"}),
            "promotions": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }



User = get_user_model()


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "No user is associated with this email address."
            )
        return email

from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Current Password'
        })
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        })
    )
## create a new card form for adding payment method