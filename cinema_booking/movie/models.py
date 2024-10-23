from django.db import models

# Create your models here.


class Theatre(models.Model):
    theatre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def add_theatre(self, name):
        theatre = Theatre(name=name)
        theatre.save()
        return theatre

    def update_theatre(self, name):
        self.name = name
        self.save()

    def get_theatre_details(self):
        return {
            "theatre_id": self.theatre_id,
            "name": self.name
        }

class Showroom(models.Model):
    showroom_id = models.AutoField(primary_key=True)
    seat_count = models.IntegerField()
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)

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

class Screening(models.Model):
    screening_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)  # This will delete screenings when the movie is deleted
    showrooms = models.ForeignKey('Showroom', on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def schedule_screening(self, movie, showroom, show_time):
        screening = Screening(movie=movie, showrooms=showroom, show_time=show_time)
        screening.save()
        return screening

    def update_screening(self, show_time):
        self.show_time = show_time
        self.save()

class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    cast = models.TextField()
    director = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    synopsis = models.TextField()
    reviews = models.TextField()
    trailer_url = models.URLField()
    rating = models.CharField(max_length=10)
    release_dates = models.JSONField()

    def add_movie(self, title, category, cast, director, producer, synopsis, reviews, trailer_url, rating, release_dates):
        movie = Movie(
            title=title,
            category=category,
            cast=cast,
            director=director,
            producer=producer,
            synopsis=synopsis,
            reviews=reviews,
            trailer_url=trailer_url,
            rating=rating,
            release_dates=release_dates
        )
        movie.save()
        return movie

    def update_movie(self, title=None, category=None, cast=None, director=None, producer=None, synopsis=None, reviews=None, trailer_url=None, rating=None, release_dates=None):
        if title:
            self.title = title
        if category:
            self.category = category
        if cast:
            self.cast = cast
        if director:
            self.director = director
        if producer:
            self.producer = producer
        if synopsis:
            self.synopsis = synopsis
        if reviews:
            self.reviews = reviews
        if trailer_url:
            self.trailer_url = trailer_url
        if rating:
            self.rating = rating
        if release_dates:
            self.release_dates = release_dates
        self.save()

    def delete_movie(self):
        self.delete()
