from . import forms, get_user_model


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "middle_name", "contact_no", "promotions"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Middle Name"}),
            "contact_no": forms.TextInput(attrs={"class": "form-control", "placeholder": "Contact Number", "required": False}),
            "promotions": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }