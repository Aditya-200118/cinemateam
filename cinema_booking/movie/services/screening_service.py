# movie/services/screening_service.py

from movie.repositories.screening_repository import ScreeningRepository
from movie.models.screening_models import Screening
from django.core.exceptions import ValidationError
from django.db.models.functions import Cast
from django.db.models import DateField
class ScreeningService:
    @staticmethod
    def schedule_screening(movie, showroom, show_time):
        """Service method to schedule a screening."""
        # Check if the screening time is already taken
        if Screening.objects.filter(showroom=showroom, show_time=show_time).exists():
            raise ValidationError("Conflict: This screening time is already taken.")
        
        screening = ScreeningRepository.create_screening(movie, showroom, show_time)
        return screening

    @staticmethod
    def update_screening(screening_id, **fields):
        """Service method to update a screening's information."""
        screening = ScreeningRepository.update_screening(screening_id, **fields)
        if not screening:
            raise ValidationError("Screening not found.")
        return screening

    @staticmethod
    def delete_screening(screening_id):
        """Service method to delete a screening."""
        if not ScreeningRepository.delete_screening(screening_id):
            raise ValidationError("Screening not found.")
        return True

    @staticmethod
    def get_screening_by_id(screening_id):
        """Service method to get a screening by ID."""
        screening = ScreeningRepository.get_screening_by_id(screening_id)
        if not screening:
            raise ValidationError("Screening not found.")
        return screening

    @staticmethod
    def list_all_screenings():
        """Service method to list all screenings."""
        return ScreeningRepository.list_screenings()
    
    @staticmethod
    def get_screenings_by_movie(movie):
        """Get screenings for a specific movie."""
        return Screening.objects.filter(movie=movie).annotate(show_date=Cast('show_time', DateField())).order_by('show_time')

    @staticmethod
    def filter_screenings_by_month(screenings, selected_month, current_date):
        """Filter screenings based on selected month."""
        if selected_month == 0:
            return screenings  # No filtering for "all months"
        elif selected_month == 1:
            return screenings.filter(show_time__month=current_date.month)  # Current month
        elif selected_month == 2:
            next_month = (current_date.month + 1) % 12
            return screenings.filter(show_time__month=next_month)  # Next month
        elif selected_month == 3:
            two_months_later = (current_date.month + 2) % 12
            return screenings.filter(show_time__month=two_months_later)  # Two months later
        return screenings

