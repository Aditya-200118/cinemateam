# booking/models/ticket_model.py

from . import *
from movie.models import Movie, Screening
class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    show_time = models.DateTimeField()
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, related_name="tickets")
    seat_number = models.IntegerField(default=0)  # Ensure this reflects the seat identification system
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ticket_type = models.ForeignKey('TicketType', on_delete=models.CASCADE, default=1)  
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="tickets")  

    def save(self, *args, **kwargs):
        self.clean()  # Call clean to enforce additional validation
        super().save(*args, **kwargs)

    def clean(self):
        # Ensure the seat number is valid for the associated showroom
        showroom = self.screening.showroom  # Assuming `showroom` is accessible from `screening`
        # chaing from from 1 based to zero based index for backend while frontend shows the 1 based index
        print(self.seat_number)
        try:
            seat_number = int(self.seat_number)
        except ValueError:
            raise ValidationError("Invalid seat number")

        if seat_number < 0 or seat_number > showroom.seat_count:
            raise ValidationError("Seat number is out of range for this showroom.")
        
        # Ensure the seat is not already booked for this screening
        if Ticket.objects.filter(screening=self.screening, seat_number=self.seat_number).exists():
            raise ValidationError("This seat is already booked for this screening.")

    def __str__(self):
        return f"Ticket {self.ticket_id} for Seat {self.seat_number} at {self.show_time} for {self.movie}"

class TicketType(models.Model):
    CHILD = 'Child'
    ADULT = 'Adult'
    SENIOR = 'Senior'

    TICKET_TYPE_CHOICES = [
        (CHILD, 'Child'),
        (ADULT, 'Adult'),
        (SENIOR, 'Senior'),
    ]

    type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.type

class MovieTicketTypeDiscount(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('movie', 'ticket_type')

    def __str__(self):
        return f"{self.ticket_type.type} discount for {self.movie.title}"

    @classmethod
    def get_discount(cls, movie_id, ticket_type_value):
        ticket_type = TicketType.objects.filter(type=ticket_type_value).first()
        if not ticket_type:
            return 0  # or
        """Returns the discount for a given movie and ticket type."""
        discount_record = cls.objects.filter(movie_id=movie_id, ticket_type=ticket_type).first()
        return discount_record.discount if discount_record else 0