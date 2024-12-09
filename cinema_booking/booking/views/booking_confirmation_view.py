# booking/views/booking_confirmation.py

from . import *
from booking.services.booking_service import BookingService

def booking_confirmation(request, booking_id):
    booking = BookingService.get_booking_by_id(booking_id)
    return render(request, 'booking/booking_confirmation.html', {'booking': booking})