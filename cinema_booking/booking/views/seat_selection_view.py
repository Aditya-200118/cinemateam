# booking/views/seat_selection.py

from . import *
from decimal import Decimal

from decimal import Decimal
from booking.services.ticket_service import MovieTicketTypeDiscountService, TicketService  # Use the service
# from booking.services.booking_service import BookingService
from booking.builder.booking_builder import BookingBuilder
from django.urls import reverse
from movie.models.screening_models import SeatLock
from django.utils.timezone import now, timedelta
from django.views.decorators.cache import never_cache
from django.contrib import messages

@never_cache
@login_required
def seat_selection(request, screening_id):
    request.session.pop('promotion_id', None)
    request.session.pop('discount_amount', None)
    request.session.pop('new_total', None)
    screening = get_object_or_404(Screening, pk=screening_id)
    movie = screening.movie
    customer = get_object_or_404(Customer, pk=request.user.pk)

    SeatLock.objects.filter(
        customer=customer,
        screening=screening,
    ).delete()
    # Fetch locked seats (valid locks only)
    locked_seats = list(
        SeatLock.objects.filter(screening=screening)
        .exclude(locked_at__lt=now() - timedelta(minutes=5))
        .values_list('seat_number', flat=True)
    )
    booked_seats = list(
        Ticket.objects.filter(screening=screening).values_list('seat_number', flat=True)
    )
    unavailable_seats = set(booked_seats) | set(locked_seats)

    # Check if any previously selected seats were released
    previously_selected_seats = request.session.get('selected_seats', [])
    expired_seats = [
        seat for seat in previously_selected_seats
        if seat not in locked_seats and seat not in booked_seats
    ]

    if expired_seats:
        # Notify the user that some seats were released
        messages.info(request, f"The following seats were released: {', '.join(expired_seats)}")
        # Clear expired seats from the session
        request.session['selected_seats'] = [
            seat for seat in previously_selected_seats if seat not in expired_seats
        ]
    senior_discount_value = MovieTicketTypeDiscountService.get_discount(movie.movie_id, TicketType.SENIOR)
    child_discount_value = MovieTicketTypeDiscountService.get_discount(movie.movie_id, TicketType.CHILD)
    # Handle POST requests for seat selection
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_seats = data.get('seats', [])
        adult_count = int(data.get('adult_count', 0))
        senior_count = int(data.get('senior_count', 0))
        child_count = int(data.get('child_count', 0))
        total_cost = float(data.get('total_cost', 0.0))

        # Validate that seat count matches ticket count
        if len(selected_seats) != (adult_count + senior_count + child_count):
            return JsonResponse({'success': False, 'error': 'Seat selection does not match ticket count.'})

        # Ensure selected seats are not already locked or booked
        if any(seat in unavailable_seats for seat in selected_seats):
            return JsonResponse({'success': False, 'error': 'One or more seats are already unavailable.'})

        # Lock the selected seats
        SeatLock.objects.filter(customer=customer, screening=screening).delete()  # Clear old locks
        SeatLock.objects.bulk_create([
            SeatLock(screening=screening, seat_number=seat, customer=customer) for seat in selected_seats
        ])

        # Store the data in the session
        request.session['selected_seats'] = selected_seats
        request.session['adult_count'] = adult_count
        request.session['senior_count'] = senior_count
        request.session['child_count'] = child_count
        request.session['total_cost'] = total_cost

        # Redirect to checkout view with the screening ID
        return JsonResponse({'success': True, 'redirect_url': reverse('checkout_process', kwargs={'screening_id': screening.screening_id})})

    # GET request handling
    ticket_type_form = TicketTypeForm(movie=movie)
    seat_count = screening.showroom.seat_count
    num_rows = ceil(seat_count / 10)
    last_row_seats = seat_count % 10 or 10
    last_row_index = num_rows - 1

    return render(request, 'booking/seat_selection.html', {
        'screening': screening,
        'ticket_type_form': ticket_type_form,
        'movie': movie,
        'adult_price': movie.price,
        'senior_discount': senior_discount_value,
        'child_discount': child_discount_value,
        'booked_seats': unavailable_seats,
        'seat_count': seat_count,
        'num_rows': num_rows,
        'last_row_seats': last_row_seats,
        'last_row_index': last_row_index,
    })
