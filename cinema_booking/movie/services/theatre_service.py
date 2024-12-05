# movie/services/theatre_service.py

from movie.repositories.theatre_repository import TheatreRepository
from django.core.exceptions import ValidationError

class TheatreService:
    @staticmethod
    def add_theatre(name):
        """Service method to add a new theatre."""
        if not name:
            raise ValidationError("Theatre name is required.")
        theatre = TheatreRepository.create_theatre(name)
        return theatre

    @staticmethod
    def update_theatre(theatre_id, name):
        """Service method to update a theatre's information."""
        theatre = TheatreRepository.update_theatre(theatre_id, name)
        if not theatre:
            raise ValidationError("Theatre not found.")
        return theatre

    @staticmethod
    def delete_theatre(theatre_id):
        """Service method to delete a theatre."""
        if not TheatreRepository.delete_theatre(theatre_id):
            raise ValidationError("Theatre not found.")
        return True

    @staticmethod
    def get_theatre_by_id(theatre_id):
        """Service method to get a theatre by its ID."""
        theatre = TheatreRepository.get_theatre_by_id(theatre_id)
        if not theatre:
            raise ValidationError("Theatre not found.")
        return theatre

    @staticmethod
    def list_all_theatres():
        """Service method to list all theatres."""
        return TheatreRepository.list_theatres()

    # @staticmethod
    # def get_theatres_by_movie(movie):
    #     return Theatre.objects.filter(showroom__screening__movie=movie).distinct()
