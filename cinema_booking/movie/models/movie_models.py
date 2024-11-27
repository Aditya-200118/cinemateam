# movie/models/movie_models.py

from . import *

class Movie(models.Model):
    MPAA_RATINGS = [ ('G', 'General Audiences'), ('PG', 'Parental Guidance Suggested'), ('PG-13', 'Parents Strongly Cautioned'), ('R', 'Restricted'), ('NC-17', 'Adults Only'), ]
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    cast = models.TextField()
    director = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    synopsis = models.TextField()
    reviews = models.TextField()
    trailer_url = models.URLField()
    rating = models.CharField(max_length=5, choices=MPAA_RATINGS)
    release_date = models.DateField(default=timezone.now)
    poster = models.ImageField(upload_to='movie/posters', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # Add price field
    duration = models.IntegerField(default=0)  # Add duration field in minutes
