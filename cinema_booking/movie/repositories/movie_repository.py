# movie/repositories/movie_repository.py

from movie.models.movie_models import Movie

class MovieRepository:
    @staticmethod
    def create_movie(title, category, cast, director, producer, synopsis, reviews, trailer_url, rating, release_date, price, duration, poster=None):
        """Create a new movie in the database."""
        movie = Movie.objects.create(
            title=title,
            category=category,
            cast=cast,
            director=director,
            producer=producer,
            synopsis=synopsis,
            reviews=reviews,
            trailer_url=trailer_url,
            rating=rating,
            release_date=release_date,
            price=price,
            duration=duration,
            poster=poster
        )
        return movie

    @staticmethod
    def get_movie_by_id(movie_id):
        """Retrieve a movie by its ID."""
        return Movie.objects.filter(movie_id=movie_id).first()

    @staticmethod
    def update_movie(movie_id, **fields):
        """Update an existing movie's details."""
        movie = MovieRepository.get_movie_by_id(movie_id)
        if movie:
            for field, value in fields.items():
                setattr(movie, field, value)
            movie.save()
            return movie
        return None

    @staticmethod
    def delete_movie(movie_id):
        """Delete a movie by its ID."""
        movie = MovieRepository.get_movie_by_id(movie_id)
        if movie:
            movie.delete()
            return True
        return False

    @staticmethod
    def list_movies():
        """List all movies in the database."""
        return Movie.objects.all()

    @staticmethod
    def filter_movies(**kwargs):
        """Filter movies based on given parameters."""
        return Movie.objects.filter(**kwargs)