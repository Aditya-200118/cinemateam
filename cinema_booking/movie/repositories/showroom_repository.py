# movie/repositories/showroom_repository.py

from movie.models.showroom_models import Showroom

class ShowroomRepository:
    @staticmethod
    def create_showroom(seat_count, theatre):
        """Create a new showroom."""
        showroom = Showroom.objects.create(seat_count=seat_count, theatre=theatre)
        return showroom

    @staticmethod
    def get_showroom_by_id(showroom_id):
        """Get showroom by ID."""
        return Showroom.objects.filter(showroom_id=showroom_id).first()

    @staticmethod
    def update_showroom(showroom_id, **fields):
        """Update showroom information."""
        showroom = ShowroomRepository.get_showroom_by_id(showroom_id)
        if showroom:
            for field, value in fields.items():
                setattr(showroom, field, value)
            showroom.save()
            return showroom
        return None

    @staticmethod
    def delete_showroom(showroom_id):
        """Delete a showroom."""
        showroom = ShowroomRepository.get_showroom_by_id(showroom_id)
        if showroom:
            showroom.delete()
            return True
        return False

    @staticmethod
    def list_showrooms():
        """List all showrooms."""
        return Showroom.objects.all()