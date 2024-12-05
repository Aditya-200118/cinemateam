# movie/repositories/screening_repository.py

from movie.models.screening_models import Screening

class ScreeningRepository:
    @staticmethod
    def create_screening(movie, showroom, show_time):
        
        screening = Screening.objects.create(movie=movie, showroom=showroom, show_time=show_time)
        return screening

    @staticmethod
    def get_screening_by_id(screening_id):
        
        return Screening.objects.filter(screening_id=screening_id).first()

    @staticmethod
    def update_screening(screening_id, **fields):
        
        screening = ScreeningRepository.get_screening_by_id(screening_id)
        if screening:
            for field, value in fields.items():
                setattr(screening, field, value)
            screening.save()
            return screening
        return None

    @staticmethod
    def delete_screening(screening_id):
        screening = ScreeningRepository.get_screening_by_id(screening_id)
        if screening:
            screening.delete()
            return True
        return False

    @staticmethod
    def list_screenings():
        """List all screenings."""
        return Screening.objects.all()
