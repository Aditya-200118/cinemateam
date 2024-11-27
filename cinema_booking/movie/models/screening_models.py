# movie/models/screening_models.py

from . import *

class Screening(models.Model):
    screening_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    @classmethod
    def schedule_screening(cls, movie, showroom, show_time):
        if cls.objects.filter(showroom=showroom, show_time=show_time).exists():
            raise ValidationError("Conflict: This screening time is already taken.")
        screening = cls(movie=movie, showroom=showroom, show_time=show_time)
        screening.save()
        return screening

    def update_show_time(self, new_show_time):
        if Screening.objects.filter(showroom=self.showroom, show_time=new_show_time).exclude(pk=self.pk).exists():
            raise ValidationError("Conflict: This screening time is already taken.")
        self.show_time = new_show_time
        self.save()

    def available_seats(self):
        Ticket = apps.get_model('booking', 'Ticket')  # Lazy load Ticket model
        all_seats = self.showroom.seats.values_list('seat_number', flat=True)
        booked_seats = Ticket.objects.filter(screening=self).values_list('seat__seat_number', flat=True)
        return [seat for seat in all_seats if seat not in booked_seats]

    def __str__(self):
        return f"Screening of {self.movie.title} at {self.show_time} in {self.showroom}"
