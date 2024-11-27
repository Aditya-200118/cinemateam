# movie/repositories/theatre_repository.py

from movie.models.theatre_models import Theatre

class TheatreRepository:
    @staticmethod
    def create_theatre(name):
        """Create a new theatre in the database."""
        theatre = Theatre.objects.create(name=name)
        return theatre

    @staticmethod
    def get_theatre_by_id(theatre_id):
        """Get a theatre by its ID."""
        return Theatre.objects.filter(theatre_id=theatre_id).first()

    @staticmethod
    def update_theatre(theatre_id, name):
        """Update the theatre's details."""
        theatre = TheatreRepository.get_theatre_by_id(theatre_id)
        if theatre:
            theatre.name = name
            theatre.save()
            return theatre
        return None

    @staticmethod
    def delete_theatre(theatre_id):
        """Delete a theatre by its ID."""
        theatre = TheatreRepository.get_theatre_by_id(theatre_id)
        if theatre:
            theatre.delete()
            return True
        return False

    @staticmethod
    def list_theatres():
        """List all theatres."""
        return Theatre.objects.all()
