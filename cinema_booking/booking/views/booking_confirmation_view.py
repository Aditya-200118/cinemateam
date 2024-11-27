# booking/views/booking_confirmation.py

from . import *
from booking.services.booking_service import BookingService
# from django.http import Http404

def booking_confirmation(request, booking_id):
    # try:
    booking = BookingService.get_booking_by_id(booking_id)
    # except Http404:
    #     return render(request, 'booking/404.html')  # Or some error page

    return render(request, 'booking/booking_confirmation.html', {'booking': booking})