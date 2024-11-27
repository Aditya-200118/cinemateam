from booking.repositories.booking_repository import BookingRepository
from booking.repositories.promotion_repository import PromotionRepository
from booking.repositories.ticket_repository import TicketRepository, MovieTicketTypeDiscountRepository, TicketTypeRepository

from django.core.exceptions import ValidationError
from decimal import Decimal