# movie/services/showroom_service.py

from movie.repositories.showroom_repository import ShowroomRepository
from django.core.exceptions import ValidationError

class ShowroomService:
    @staticmethod
    def add_showroom(seat_count, theatre):
        """Service method to add a new showroom."""
        showroom = ShowroomRepository.create_showroom(seat_count, theatre)
        return showroom

    @staticmethod
    def update_showroom(showroom_id, **fields):
        """Service method to update a showroom's details."""
        showroom = ShowroomRepository.update_showroom(showroom_id, **fields)
        if not showroom:
            raise ValidationError("Showroom not found.")
        return showroom

    @staticmethod
    def delete_showroom(showroom_id):
        """Service method to delete a showroom."""
        if not ShowroomRepository.delete_showroom(showroom_id):
            raise ValidationError("Showroom not found.")
        return True

    @staticmethod
    def list_showrooms():
        """Service method to get all showrooms."""
        return ShowroomRepository.list_showrooms()
