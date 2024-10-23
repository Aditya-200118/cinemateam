from django.test import TestCase

# Create your tests here.


from movie.models import Movie 
 # Use the actual name of your Django app if it's different
# Create dummy movie data
movies = [
    {
        "title": "The Shawshank Redemption",
        "category": "Drama",
        "cast": "Tim Robbins, Morgan Freeman",
        "director": "Frank Darabont",
        "producer": "Niki Marvin",
        "synopsis": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "reviews": "Excellent",
        "trailer_url": "https://www.youtube.com/embed/6hB3S9bIaco",
        "rating": "R",
        "release_dates": {"US": "1994-09-23"}
    },
    {
        "title": "Inception",
        "category": "Sci-Fi, Thriller",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt",
        "director": "Christopher Nolan",
        "producer": "Emma Thomas, Christopher Nolan",
        "synopsis": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "reviews": "Mind-bending",
        "trailer_url": "https://www.youtube.com/embed/YoHD9XEInc0",
        "rating": "PG-13",
        "release_dates": {"US": "2010-07-16"}
    },
    {
        "title": "The Dark Knight",
        "category": "Action, Crime, Drama",
        "cast": "Christian Bale, Heath Ledger",
        "director": "Christopher Nolan",
        "producer": "Emma Thomas, Charles Roven, Christopher Nolan",
        "synopsis": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
        "reviews": "Outstanding",
        "trailer_url": "https://www.youtube.com/embed/EXeTwQWrcwY",
        "rating": "PG-13",
        "release_dates": {"US": "2008-07-18"}
    },
    {
        "title": "The Matrix",
        "category": "Action, Sci-Fi",
        "cast": "Keanu Reeves, Laurence Fishburne",
        "director": "Lana Wachowski, Lilly Wachowski",
        "producer": "Joel Silver",
        "synopsis": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "reviews": "Revolutionary",
        "trailer_url": "https://www.youtube.com/embed/vKQi3bBA1y8",
        "rating": "R",
        "release_dates": {"US": "1999-03-31"}
    },
    {
        "title": "Interstellar",
        "category": "Adventure, Drama, Sci-Fi",
        "cast": "Matthew McConaughey, Anne Hathaway",
        "director": "Christopher Nolan",
        "producer": "Emma Thomas, Christopher Nolan, Lynda Obst",
        "synopsis": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "reviews": "Epic",
        "trailer_url": "https://www.youtube.com/embed/zSWdZVtXT7E",
        "rating": "PG-13",
        "release_dates": {"US": "2014-11-07"}
    }
]

# Insert dummy movie data into the database
for movie_data in movies:
    movie = Movie(
        title=movie_data["title"],
        category=movie_data["category"],
        cast=movie_data["cast"],
        director=movie_data["director"],
        producer=movie_data["producer"],
        synopsis=movie_data["synopsis"],
        reviews=movie_data["reviews"],
        trailer_url=movie_data["trailer_url"],
        rating=movie_data["rating"],
        release_dates=movie_data["release_dates"]
    )
    movie.save()


from movie.models import Theatre, Showroom, Movie, Screening
from django.utils import timezone
import datetime

# Create a theatre
theatre = Theatre.objects.create(name="Main Theatre")

# Create a showroom
showroom = Showroom.objects.create(seat_count=100, theatre=theatre)


# Get the movies
shawshank = Movie.objects.get(title="The Shawshank Redemption")
inception = Movie.objects.get(title="Inception")
dark_knight = Movie.objects.get(title="The Dark Knight")
matrix = Movie.objects.get(title="The Matrix")
interstellar = Movie.objects.get(title="Interstellar")

# Create screening data
screenings = [
    {
        "movie": shawshank,
        "showroom": showroom,
        "show_time": timezone.now() + datetime.timedelta(days=1, hours=14)  # Tomorrow at 2 PM
    },
    {
        "movie": inception,
        "showroom": showroom,
        "show_time": timezone.now() + datetime.timedelta(days=2, hours=16)  # Day after tomorrow at 4 PM
    },
    {
        "movie": dark_knight,
        "showroom": showroom,
        "show_time": timezone.now() + datetime.timedelta(days=3, hours=18)  # In three days at 6 PM
    },
    {
        "movie": matrix,
        "showroom": showroom,
        "show_time": timezone.now() + datetime.timedelta(days=4, hours=20)  # In four days at 8 PM
    },
    {
        "movie": interstellar,
        "showroom": showroom,
        "show_time": timezone.now() + datetime.timedelta(days=5, hours=22)  # In five days at 10 PM
    }
]

# Insert dummy screening data into the database
for screening_data in screenings:
    screening = Screening(
        movie=screening_data["movie"],
        showrooms=screening_data["showroom"],
        show_time=screening_data["show_time"]
    )
    screening.save()
