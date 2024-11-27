from . import *
from booking.models import MovieTicketTypeDiscount, TicketType

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['movie', 'screening', 'seat_number', 'price']  # Removed 'show_time' and 'seat_number'


class TicketTypeForm(forms.Form):
    adult_count = forms.IntegerField(
        min_value=0,
        initial=0,
        label='Adults',
        widget=forms.NumberInput(attrs={'placeholder': 'Enter number of adults', 'class': 'form-control'})
    )
    senior_count = forms.IntegerField(
        min_value=0,
        initial=0,
        label='Seniors',
        widget=forms.NumberInput(attrs={'placeholder': 'Enter number of seniors', 'class': 'form-control'})
    )
    child_count = forms.IntegerField(
        min_value=0,
        initial=0,
        label='Children',
        widget=forms.NumberInput(attrs={'placeholder': 'Enter number of children', 'class': 'form-control'})
    )
    total_cost = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        initial=0,
        label='Total Cost',
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )

    def __init__(self, *args, movie=None, **kwargs):
        self.movie = movie
        super().__init__(*args, **kwargs)

    def calculate_total_cost(self):
        """Calculate the total cost based on ticket counts and discounts."""
        if not self.movie:
            return 0

        adult_count = self.cleaned_data.get('adult_count', 0)
        senior_count = self.cleaned_data.get('senior_count', 0)
        child_count = self.cleaned_data.get('child_count', 0)

        # Base ticket price
        adult_price = self.movie.price

        # Retrieve discounts using the new get_discount method
        senior_discount_rate = MovieTicketTypeDiscount.get_discount(
            movie_id=self.movie.movie_id,
            ticket_type_value=TicketType.objects.get(type=TicketType.SENIOR).id
        )
        child_discount_rate = MovieTicketTypeDiscount.get_discount(
            movie_id=self.movie.movie_id,
            ticket_type_value=TicketType.objects.get(type=TicketType.CHILD).id
        )

        # Calculate discounted prices
        senior_price = adult_price * (1 - senior_discount_rate // 100)
        child_price = adult_price * (1 - child_discount_rate // 100)

        # Calculate the total cost based on counts and prices
        total_cost = (adult_count * adult_price) + (senior_count * senior_price) + (child_count * child_price)
        return total_cost

    def clean(self):
        """Clean the form data and set the total_cost."""
        cleaned_data = super().clean()
        if self.is_valid():
            cleaned_data['total_cost'] = self.calculate_total_cost()
        return cleaned_data

class MonthDayForm(forms.Form):
    current_month_index = datetime.now().month - 1 
    next_month_index = (current_month_index + 1)%12
    month_after_next_index = (current_month_index + 2)%12
    LIST_OF_MONTH = [
        'January', 
        'February', 
        'March', 
        'April', 
        'May', 
        'June', 
        'July', 
        'August', 
        'Septemeber', 
        'October', 
        'November', 
        'December'
    ]
    MONTH_CHOICES = [
        (0, 'Show All'),
        (1, str(LIST_OF_MONTH[current_month_index])), 
        (2, str(LIST_OF_MONTH[next_month_index])), 
        (3, str(LIST_OF_MONTH[month_after_next_index])),
    ]
    DAY_CHOICES = [
        ('all', 'All Days'), 
        ('sunday', 'Sunday'), 
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    ]

    selected_month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.RadioSelect, initial=0)
    selected_day = forms.ChoiceField(choices=DAY_CHOICES, widget=forms.RadioSelect, initial='all')
    
class SeatSelectionForm(forms.Form):
    selected_seats = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean_selected_seats(self):
        seats = self.cleaned_data.get('selected_seats', '')
        if seats:
            return seats.split(',')  # Assume seats are sent as a comma-separated string
        return []