from . import *
from booking.services.booking_service import BookingService
from booking.services.ticket_service import TicketService
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def order_history(request):
    customer = get_object_or_404(Customer, pk = request.user.pk)  # Assuming `request.user` is linked to `Customer`
    try:
        bookings = BookingService.get_order_history_for_customer(customer)
    except ValidationError:
        bookings = []  # No bookings found, return an empty list
        messages.info(request, "You have no past bookings.")  # Add the message to the messages framework

    return render(request, "accounts/order_history.html", {
        "order_history": bookings,
    })

def get_tickets_for_booking(request, booking_id):
    print(f"here is the ticket data: ")
    tickets = TicketService.get_all_tickets_for_booking(booking_id)
    ticket_data = [
        {
            "ticket_id": ticket.ticket_id,
            "seat_number": ticket.seat_number,
            "ticket_type": ticket.ticket_type.type,
            "price": ticket.price,
            "show_time": ticket.show_time
        }
        for ticket in tickets
    ]    
    return JsonResponse({"tickets": ticket_data})