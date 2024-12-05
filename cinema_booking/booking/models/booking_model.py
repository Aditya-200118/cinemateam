# booking/models/booking_model.py

from . import *
from accounts.models import Customer

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    show_time = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def create_booking(self):
        # Calculate total price based on associated tickets
        self.total_price = sum(ticket.price for ticket in self.tickets.all())
        self.save()

    def cancel_booking(self):
        # Logic to cancel a booking
        pass

    def apply_promotion(self, promo_code):
        # Logic to apply a promotion
        pass