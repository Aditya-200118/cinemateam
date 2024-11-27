from django import forms
from django.core.exceptions import ValidationError
from booking.models import Booking, Promotion, Ticket
from datetime import datetime

from .booking_forms import BookingForm
from .promotion_forms import PromotionForm, CouponForm
from .ticket_forms import TicketForm, TicketTypeForm, MonthDayForm, SeatSelectionForm