# movie/models/showroom_models.py

from . import *

class Showroom(models.Model):
    showroom_id = models.AutoField(primary_key=True)
    seat_count = models.IntegerField(default=100)
    name = models.CharField(max_length=100, null=True, blank=True) 
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)

    def get_available_seats(self):
        Ticket = apps.get_model('booking', 'Ticket')
        booked_seats = Ticket.objects.filter(screening__showroom=self).values_list('seat_number', flat=True)
        return [seat for seat in range(1, self.seat_count + 1) if seat not in booked_seats]

    def add_showroom(self, seat_count, theatre):
        showroom = Showroom(seat_count=seat_count, theatre=theatre)
        showroom.save()
        return showroom

    def get_showroom_info(self):
        return {
            "showroom_id": self.showroom_id,
            "seat_count": self.seat_count,
            "theatre": self.theatre.get_theatre_details()
        }

    def update_showroom(self, seat_count):
        self.seat_count = seat_count
        self.save()

    def __str__(self):
        return f'Showroom {self.name}, id: {self.showroom_id} in theatre: {self.theatre.name}'
    