# booking/services/ticket_service.py

from . import TicketRepository, ValidationError, MovieTicketTypeDiscountRepository, TicketTypeRepository, Decimal

class TicketService:
    @staticmethod
    def create_ticket_for_booking(movie, show_time, screening, seat_number, price, ticket_type, booking, showroom):
        ticket = TicketRepository.create_ticket(movie, show_time, screening, seat_number, price, ticket_type, booking, showroom)
        if not ticket:
            raise ValidationError("Failed to create ticket.")
        return ticket

    @staticmethod
    def cancel_ticket(ticket_id):
        if not TicketRepository.cancel_ticket(ticket_id):
            raise ValidationError("Failed to cancel ticket.")
        return True
    
    @staticmethod
    def get_all_tickets_for_booking(booking_id):

        tickets = TicketRepository.get_all_tickets_for_booking(booking_id)
        if not tickets:
            raise ValidationError("No tickets found for this booking.")
        return tickets

class MovieTicketTypeDiscountService:
    
    @staticmethod
    def get_discount(movie, ticket_type_value):

        ticket_type = TicketTypeRepository.get_ticket_type(ticket_type_value)
        
        if not ticket_type:
            return Decimal(0)
        
        discount_record = MovieTicketTypeDiscountRepository.get_discount(movie, ticket_type)

        return discount_record.discount if discount_record else Decimal(0)

    @staticmethod
    def create_discount(movie, ticket_type_value, discount_value):

        ticket_type = TicketTypeRepository.get_ticket_type(ticket_type_value)
        
        if not ticket_type:
            raise ValueError("Invalid ticket type value.")

        discount_record = MovieTicketTypeDiscountRepository.create_discount(movie, ticket_type, discount_value)
        
        return discount_record
