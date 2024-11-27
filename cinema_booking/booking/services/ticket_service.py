# booking/services/ticket_service.py

from . import TicketRepository, ValidationError, MovieTicketTypeDiscountRepository, TicketTypeRepository, Decimal

class TicketService:
    @staticmethod
    def create_ticket_for_booking(movie, show_time, screening, seat_number, price, ticket_type, booking):
        ticket = TicketRepository.create_ticket(movie, show_time, screening, seat_number, price, ticket_type, booking)
        if not ticket:
            raise ValidationError("Failed to create ticket.")
        return ticket

    @staticmethod
    def cancel_ticket(ticket_id):
        if not TicketRepository.cancel_ticket(ticket_id):
            raise ValidationError("Failed to cancel ticket.")
        return True

class MovieTicketTypeDiscountService:
    
    @staticmethod
    def get_discount(movie, ticket_type_value):
        """
        Retrieves the discount for a specific movie and ticket type.
        Args:
            movie: Movie object.
            ticket_type_value: A string representing the ticket type (e.g., 'Child', 'Senior', 'Adult').

        Returns:
            Decimal: The discount for the given movie and ticket type, or 0 if no discount is found.
        """
        # Fetch the TicketType object using the repository
        ticket_type = TicketTypeRepository.get_ticket_type(ticket_type_value)
        
        if not ticket_type:
            return Decimal(0)  # If no ticket type found, return no discount
        
        # Fetch the discount record using the repository
        discount_record = MovieTicketTypeDiscountRepository.get_discount(movie, ticket_type)
        
        # Return the discount if found, otherwise 0
        return discount_record.discount if discount_record else Decimal(0)

    @staticmethod
    def create_discount(movie, ticket_type_value, discount_value):
        """
        Creates a new discount record for a movie and ticket type.
        Args:
            movie: Movie object to associate the discount with.
            ticket_type_value: A string representing the ticket type (e.g., 'Child', 'Senior', 'Adult').
            discount_value: The discount percentage to set for the ticket type.
        
        Returns:
            MovieTicketTypeDiscount: The newly created or updated discount record.
        """
        # Fetch the TicketType object
        ticket_type = TicketTypeRepository.get_ticket_type(ticket_type_value)
        
        if not ticket_type:
            raise ValueError("Invalid ticket type value.")

        # Create or update the discount record using the repository
        discount_record = MovieTicketTypeDiscountRepository.create_discount(movie, ticket_type, discount_value)
        
        return discount_record
