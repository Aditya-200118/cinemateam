# admin/admin_forms.py

from . import *

class TheatreForm(forms.ModelForm):
    # Existing Theatre Selection
    existing_theatre = forms.ModelChoiceField(
        queryset=Theatre.objects.all(),
        required=True,  # Make this field required since we are not allowing new theatres
        empty_label="Select Existing Theatre",  # Display text for empty selection
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Theatre
        fields = ['existing_theatre']
        labels = {'existing_theatre': 'Select an Existing Theatre'}

    def clean(self):
        cleaned_data = super().clean()
        existing_theatre = cleaned_data.get("existing_theatre")
        
        if not existing_theatre:
            raise forms.ValidationError("You must select an existing theatre.")
        
        return cleaned_data



class ShowroomForm(forms.ModelForm):
    # Dropdown to select an existing showroom
    existing_showroom = forms.ModelChoiceField(
        queryset=Showroom.objects.all(),
        required=True,  # Ensure this field is required
        empty_label="Select Existing Showroom",  # Placeholder text when no showroom is selected
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Showroom
        fields = ['existing_showroom']  # Only include the field for selecting an existing showroom

    def __init__(self, *args, **kwargs):
        super(ShowroomForm, self).__init__(*args, **kwargs)
        # Explicitly refresh the queryset for the existing_showroom field
        self.fields['existing_showroom'].queryset = Showroom.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        existing_showroom = cleaned_data.get("existing_showroom")
        
        # Validate that an existing showroom has been selected
        if not existing_showroom:
            raise forms.ValidationError("You must select an existing showroom.")
        
        return cleaned_data


from django import forms
# from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title', 'category', 'cast', 'director', 'producer', 'synopsis', 'reviews', 'trailer_url',
            'rating', 'release_date', 'price', 'poster', 'duration'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie Title'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'cast': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cast'}),
            'director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Director'}),
            'producer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Producer'}),
            'synopsis': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Synopsis'}),
            'reviews': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Reviews'}),
            'trailer_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Trailer URL'}),
            'release_date': forms.SelectDateWidget(
                years=range(timezone.now().year - 10, timezone.now().year + 5),
                attrs={'class': 'form-control'}
            ),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ticket Price'}),
            'poster': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in minutes'}),
        }

    rating = forms.ChoiceField(
        choices=Movie.MPAA_RATINGS,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Rating'})
    )

class ScreeningForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Accept showroom as an argument and set it as an attribute
        self.showroom = kwargs.pop('showroom', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Screening
        fields = ['show_time']
        widgets = {
            'show_time': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': 'Screening Time'}
            ),
        }

    def clean_show_time(self):
        print("Cleaning show time")
        show_time = self.cleaned_data['show_time']

        # Use the showroom passed to the form explicitly (from __init__)
        if not self.showroom:
            raise ValidationError("A showroom must be selected before setting a show time.")

        # Validate that no other screening exists for the same time in the same showroom
        if Screening.objects.filter(showroom=self.showroom, show_time=show_time).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A screening is already scheduled at this time in this showroom.")

        return show_time
    
class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['promo_code', 'title', 'description', 'discount', 'valid_from', 'valid_to']
