# booking/services/booking_service.py
from . import BookingRepository, TicketRepository, ValidationError

class BookingService:
    @staticmethod
    def create_booking_for_customer(customer, show_time, showroom):
        # Call repository to create the booking
        booking = BookingRepository.create_booking(customer, show_time, showroom)
        if not booking:
            raise ValidationError("Failed to create booking.")
        return booking
    
    @staticmethod
    def cancel_booking(booking_id):
        booking = BookingRepository.get_booking_by_id(booking_id)
        if not booking:
            raise ValidationError("Booking not found.")
        
        # Remove associated tickets before canceling
        for ticket in TicketRepository.get_all_tickets_for_booking(booking):
            TicketRepository.cancel_ticket(ticket.id)
        
        return BookingRepository.delete_booking(booking_id)
    
    @staticmethod
    def apply_promotion(booking_id, promo_code):
        booking = BookingRepository.get_booking_by_id(booking_id)
        if not booking:
            raise ValidationError("Booking not found.")
        
        updated_booking = BookingRepository.apply_promotion_to_booking(booking, promo_code)
        if not updated_booking:
            raise ValidationError("Promotion code is invalid.")
        
        return updated_booking
    
    @staticmethod
    def get_booking_by_id(booking_id):
        # Fetch booking using repository
        booking = BookingRepository.get_booking_by_id(booking_id)
        if not booking:
            raise ValidationError("Booking not found.")
        return booking
    
    @staticmethod
    def get_order_history_for_customer(customer):
        bookings = BookingRepository.get_all_bookings_for_customer(customer)
        if not bookings.exists():
            raise ValidationError("No order history found for the customer.")
        return bookings