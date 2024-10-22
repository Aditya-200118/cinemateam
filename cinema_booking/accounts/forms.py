from django import forms
from django.contrib.auth import get_user_model
from .models import Card, Address
from django.core.exceptions import ValidationError

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


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        ),
    )

    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Repeat password", "class": "form-control"}
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ["first_name", "middle_name", "last_name", "contact_no", "email"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "middle_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Middle Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "contact_no": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Contact Number"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]

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


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_number', 'expiry_date', 'cvv']

    def __init__(self, *args, **kwargs):
        self.is_registration = kwargs.pop('is_registration', False)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not self.is_registration:
            customer = self.instance.customer
            if customer.cards.count() >= 4:
                raise ValidationError("You cannot store more than 4 payment cards.")
        return cleaned_data

# from .models import Customer
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'contact_no', 'promotions']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'promotions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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