# booking/views/booking_confirmation.py
from accounts.services.email_proxy import DjangoEmailService, EmailProxy

from . import *
from booking.services.booking_service import BookingService

def booking_confirmation(request, booking_id):
    booking = BookingService.get_booking_by_id(booking_id)
    customer = Customer.objects.get(pk=request.user.pk)
    email_service = EmailProxy(DjangoEmailService())
    email_service.send_email(
                    subject="Booking Confirmed",
                    message="Your booking is confirmed.",
                    recipient_list=[customer.email],
                )
    return render(request, 'booking/booking_confirmation.html', {'booking': booking})