# accounts/forms/customer_auth_forms.py

from . import *
from django import forms
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"placeholder": "Email address", "class": "form-control", "id":"email"}
        ),
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control", "id":"password"}
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
                    "id":"first_name",
                    "required": True,
                }
            ),
            "middle_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Middle Name", "id": "middle_name"}
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last Name",
                    "id":"last_name",
                    "required": True,
                }
            ),
            "contact_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Contact Number",
                    "id":"contact_number",
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