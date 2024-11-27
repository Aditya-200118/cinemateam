# booking/repositories/ticket_repository.py

from booking.models import Ticket, MovieTicketTypeDiscount, TicketType
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

class TicketRepository:
    @staticmethod
    def create_ticket(movie, show_time, screening, seat_number, price, ticket_type, booking):
        try:
            ticket = Ticket.objects.create(
                movie=movie,
                show_time=show_time,
                screening = screening,
                seat_number=seat_number,
                price = price,
                ticket_type=ticket_type,
                booking=booking,
            )
            return ticket
        except IntegrityError:
            return None  # In case of an integrity error
    
    @staticmethod
    def get_ticket_by_id(ticket_id):
        try:
            return Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_tickets_for_booking(booking):
        return Ticket.objects.filter(booking=booking)

    @staticmethod
    def cancel_ticket(ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.delete()
            return True
        except Ticket.DoesNotExist:
            return False
        

class MovieTicketTypeDiscountRepository:
    
    @staticmethod
    def get_discount(movie, ticket_type):
        """
        Fetch the discount record for the given movie and ticket type.
        Args:
            movie: Movie object.
            ticket_type: TicketType object.

        Returns:
            MovieTicketTypeDiscount: Discount record if found, else None.
        """
        try:
            discount_record = MovieTicketTypeDiscount.objects.get(movie=movie, ticket_type=ticket_type)
            return discount_record
        except ObjectDoesNotExist:
            return None  # No discount found for the given movie and ticket type

    @staticmethod
    def create_discount(movie, ticket_type, discount_value):
        """
        Creates a new discount or updates the existing one for the given movie and ticket type.
        Args:
            movie: Movie object.
            ticket_type: TicketType object.
            discount_value: Decimal value for the discount.

        Returns:
            MovieTicketTypeDiscount: The created or updated discount record.
        """
        discount_record, created = MovieTicketTypeDiscount.objects.update_or_create(
            movie=movie,
            ticket_type=ticket_type,
            defaults={'discount': discount_value}
        )
        return discount_record

class TicketTypeRepository:

    @staticmethod
    def get_ticket_type(ticket_type_value):
        """
        Fetches the TicketType object for the given ticket type value (e.g., 'Child', 'Senior', 'Adult').
        Args:
            ticket_type_value: A string representing the ticket type (e.g., 'Child', 'Senior', 'Adult').

        Returns:
            TicketType: TicketType object if found, else None.
        """
        try:
            ticket_type = TicketType.objects.get(type=ticket_type_value)
            return ticket_type
        except ObjectDoesNotExist:
            return None  # No ticket type found for the given value
