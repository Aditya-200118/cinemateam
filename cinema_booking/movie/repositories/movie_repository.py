# movie/repositories/movie_repository.py

from movie.models.movie_models import Movie

class MovieRepository:
    @staticmethod
    def create_movie(title, category, cast, director, producer, synopsis, reviews, trailer_url, rating, release_date, price, duration, poster=None):
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
        return Movie.objects.filter(movie_id=movie_id).first()

    @staticmethod
    def update_movie(movie_id, **fields):
        movie = MovieRepository.get_movie_by_id(movie_id)
        if movie:
            for field, value in fields.items():
                setattr(movie, field, value)
            movie.save()
            return movie
        return None

    @staticmethod
    def delete_movie(movie_id):
        movie = MovieRepository.get_movie_by_id(movie_id)
        if movie:
            movie.delete()
            return True
        return False

    @staticmethod
    def list_movies():
        return Movie.objects.all()

    @staticmethod
    def filter_movies(**kwargs):
        return Movie.objects.filter(**kwargs)