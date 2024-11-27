# booking/builders/booking_builder.py

from booking.services.booking_service import BookingService
from booking.services.promotion_service import PromotionService
from booking.services.ticket_service import TicketService
from decimal import Decimal

class BookingBuilder:
    def __init__(self, customer, screening):
        self.customer = customer
        self.screening = screening
        self.booking = None
        self.tickets = []
        self.total_cost = Decimal(0)
        self.promotion = None

    def create_booking(self):
        self.booking = BookingService.create_booking_for_customer(self.customer, self.screening.show_time)
        return self

    def apply_promotion(self, promo_code):
        """Apply a promotion code to the booking."""
        if not self.customer:
            raise Exception("Customer must be set to apply a promotion.")
        print(f"Apply Promotion is will call the service now for validate_and_use_coupon: {promo_code}")
        # Validate and use the coupon
        self.promotion = PromotionService.validate_and_use_coupon(self.customer, promo_code)
        return self

    def calculate_discounted_price(self, base_price):
        if self.promotion:
            discount_percentage = Decimal(self.promotion.discount) / Decimal(100)
            return base_price * (1 - discount_percentage)
        return base_price

    def add_ticket(self, movie, show_time, screening, seat_number, price, ticket_type):
        if not self.booking:
            raise Exception("Booking must be created before adding tickets.")

        discounted_price = self.calculate_discounted_price(Decimal(price))
        ticket = TicketService.create_ticket_for_booking(
            movie=movie,
            show_time=show_time,
            screening=screening,
            seat_number=seat_number,
            price=discounted_price,
            ticket_type=ticket_type,
            booking=self.booking
        )
        self.tickets.append(ticket)
        self.total_cost += discounted_price
        return self

    def finalize(self):
        if not self.booking:
            raise Exception("Booking must be created before finalizing.")
        self.booking.total_price = self.total_cost
        self.booking.save()
        return self.booking

