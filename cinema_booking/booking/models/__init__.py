from django.db import models
from django.core.exceptions import ValidationError
import logging
from django.conf import settings

from .booking_model import Booking
from .promotion_model import Promotion
from .ticket_model import Ticket, TicketType, MovieTicketTypeDiscount