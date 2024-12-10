# booking/models/booking_model.py

from . import *
from accounts.models import Customer
# from django.apps import apps 
from movie.models.showroom_models import Showroom

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    show_time = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)  # Add this line

    def create_booking(self):
        # Calculate total price based on associated tickets
        self.total_price = sum(ticket.price for ticket in self.tickets.all())
        self.save()