from django.db import models

# Create your models here.


class Theatre(models.Model):
    theatre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # showrooms = models.OneToManyField('Showroom') this doesnt exist hence we will use a foreign key in Showroom class
    
    def add_theatre(self):
        pass

    def update_theatre(self):
        pass

    def get_theatre_details(self):
        pass

class Showroom(models.Model):
    showroom_id = models.AutoField(primary_key=True)
    seat_count = models.IntegerField()
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE) # this is the foreign key relation allowing us to map a showroom to theatre
    def add_showroom(self):
        pass
    def get_showroom_info(self):
        pass
    def update_showroom(self):
        pass

class Screening(models.Model):
    screening_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE) # this needs to be checked for correctness
    showrooms = models.ForeignKey('Showroom', on_delete=models.CASCADE) # this needs to be checked for correctness
    show_time = models.DateTimeField()
    def schedule_screening(self):
        pass
    def update_screening(self):
        pass

class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    cast = models.TextField()
    director = models.CharField(max_length=50)
    producer = models.CharField(max_length = 50)
    synopsis = models.TextField()
    reviews = models.TextField()
    trailer_url = models.URLField()
    rating = models.CharField(max_length=10)
    release_dates = models.JSONField()
    
    def add_movie(self):
        pass
    def update_movie(self):
        pass
    
    def delete_movie(self):
        pass