# booking/repositories/booking_repository.py

from booking.models import Booking, Ticket, Promotion
from django.db import IntegrityError

class BookingRepository:
    @staticmethod
    def create_booking(customer, show_time, showroom):
        try:
            booking = Booking.objects.create(customer=customer, show_time=show_time, showroom=showroom)
            return booking
        except IntegrityError:
            return None  # In case of an integrity error, such as a foreign key issue

    
    @staticmethod
    def get_booking_by_id(booking_id):
        try:
            return Booking.objects.get(booking_id=booking_id)
        except Booking.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_bookings_for_customer(customer):
        return Booking.objects.filter(customer=customer)
    
    @staticmethod
    def delete_booking(booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.delete()
            return True
        except Booking.DoesNotExist:
            return False
    
    @staticmethod
    def apply_promotion_to_booking(booking, promo_code):
        try:
            promotion = Promotion.objects.get(promo_code=promo_code)
            booking.total_price -= (booking.total_price * (promotion.discount / 100))
            booking.save()
            return booking
        except Promotion.DoesNotExist:
            return None