# movie/services/movie_service.py

from movie.repositories.movie_repository import MovieRepository
from movie.models.movie_models import Movie
from django.core.exceptions import ValidationError
from django.utils import timezone
class MovieService:
    @staticmethod
    def add_movie(title, category, cast, director, producer, synopsis, reviews, trailer_url, rating, release_date, price, duration, poster=None):
        # Add any business logic if needed
        if not title or not category:
            raise ValidationError("Title and Category are required fields.")

        movie = MovieRepository.create_movie(
            title, category, cast, director, producer, synopsis, reviews, trailer_url, rating, release_date, price, duration, poster
        )
        return movie

    @staticmethod
    def update_movie(movie_id, **fields):
        movie = MovieRepository.update_movie(movie_id, **fields)
        if not movie:
            raise ValidationError("Movie not found.")
        return movie

    @staticmethod
    def delete_movie(movie_id):
        if not MovieRepository.delete_movie(movie_id):
            raise ValidationError("Movie not found or could not be deleted.")
        return True

    @staticmethod
    def get_movie_by_id(movie_id):
        movie = MovieRepository.get_movie_by_id(movie_id)
        if not movie:
            raise ValidationError("Movie not found.")
        return movie

    @staticmethod
    def list_all_movies():
        return MovieRepository.list_movies()
    
    @staticmethod
    def get_now_playing_movies(search_query=None):

        today = timezone.now().date()
        if search_query:
            return MovieRepository.filter_movies(title__icontains=search_query, release_date__lte=today)
        return MovieRepository.filter_movies(release_date__lte=today)

    @staticmethod
    def get_coming_soon_movies(search_query=None):
        today = timezone.now().date()
        if search_query:
            return MovieRepository.filter_movies(title__icontains=search_query, release_date__gt=today)
        return MovieRepository.filter_movies(release_date__gt=today)
    
    @staticmethod
    def get_movies_by_title(search_query):
        today = timezone.now().date()
        return MovieRepository.filter_movies(title__icontains=search_query, release_date__lte=today)

    @staticmethod
    def get_movies_by_category(search_query):
        today = timezone.now().date()
        return MovieRepository.filter_movies(category__icontains=search_query, release_date__lte=today)

    @staticmethod
    def get_now_playing_by_category(category):
        if not category:
            raise ValidationError("Category is required.")

        today = timezone.now().date()
        return MovieRepository.filter_movies(category__icontains=category, release_date__lte=today)

    @staticmethod
    def get_coming_soon_by_category(category):
        if not category:
            raise ValidationError("Category is required.")

        today = timezone.now().date()
        return MovieRepository.filter_movies(category__icontains=category, release_date__gt=today)
    
    @staticmethod
    def get_now_playing_by_title(title):
        if not title:
            raise ValidationError("Title is required.")
        today = timezone.now().date()
        
        return MovieRepository.filter_movies(title__icontains=title, release_date__lte=today)

    @staticmethod
    def get_coming_soon_by_title(title):
        if not title:
            raise ValidationError("Title is required.")
        today = timezone.now().date()

        return MovieRepository.filter_movies(title__icontains=title, release_date__gt=today)

