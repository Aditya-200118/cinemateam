from . import *

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer']