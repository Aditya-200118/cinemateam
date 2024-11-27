# views.py

from . import *
from decimal import Decimal
from booking.services.ticket_service import MovieTicketTypeDiscountService
from booking.services.promotion_service import PromotionService
from accounts.services.transcation_service import TransactionService
from booking.builder.booking_builder import BookingBuilder
from accounts.services.card_service import CardService
# from booking.forms import CouponForm
from django.contrib import messages
from accounts.models import Card
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from booking.models.promotion_model import CouponUsage

@login_required
def checkout(request, screening_id):

    screening = get_object_or_404(Screening, pk=screening_id)
    movie = screening.movie
    customer = get_object_or_404(Customer, pk=request.user.pk)

    selected_seats = request.session.get('selected_seats', [])
    adult_count = int(request.session.get('adult_count', 0))
    senior_count = int(request.session.get('senior_count', 0))
    child_count = int(request.session.get('child_count', 0))

    senior_discount_value = MovieTicketTypeDiscountService.get_discount(movie.movie_id, TicketType.SENIOR)
    child_discount_value = MovieTicketTypeDiscountService.get_discount(movie.movie_id, TicketType.CHILD)

    senior_price = movie.price * (1 - Decimal(senior_discount_value) / Decimal(100))
    child_price = movie.price * (1 - Decimal(child_discount_value) / Decimal(100))

    promotion = None
    if 'promotion_id' in request.session:
        promotion = PromotionService.get_promotion_by_code(request.session['promotion_id'])

    if request.method == 'POST':
        try:
            # Build the booking using the BookingBuilder pattern
            builder = BookingBuilder(customer, screening).create_booking()

            # Apply promotion if available
            if promotion:
                builder.apply_promotion(promotion)
            else:
                messages.warning(request, "No coupon was applied. Proceeding without a discount.")

            # Add tickets to the booking
            for i, seat_number in enumerate(selected_seats):
                if i < adult_count:
                    ticket_type = TicketType.objects.get(type=TicketType.ADULT)
                    price = movie.price
                elif i < adult_count + senior_count:
                    ticket_type = TicketType.objects.get(type=TicketType.SENIOR)
                    price = senior_price
                else:
                    ticket_type = TicketType.objects.get(type=TicketType.CHILD)
                    price = child_price

                builder.add_ticket(
                    movie=movie,
                    show_time=screening.show_time,
                    screening=screening,
                    seat_number=seat_number,
                    price=price,
                    ticket_type=ticket_type
                )

            # Clear coupon-related session data after successful booking
            request.session.pop('promotion_id', None)
            request.session.pop('discount_amount', None)
            request.session.pop('new_total', None)

            # Retrieve selected card ID from session
            card_id = request.session.get('selected_card_id', None)
            if not card_id:
                messages.error(request, "Please select a saved card to proceed with the payment.")
                return redirect('checkout_process', screening_id=screening_id)

            # Fetch the card object using the card ID
            card = Card.objects.filter(id=card_id, customer=customer).first()
            if not card:
                messages.error(request, "Invalid card selected.")
                return redirect('checkout_process', screening_id=screening_id)

            # Finalize the booking and record the transaction
            booking = builder.finalize()
            payment_amount = Decimal(request.session.get('total_cost', 0.0))
            transaction_service = TransactionService()
            transaction_service.create_transaction(customer, booking, card.card_number, payment_amount)

            return redirect('booking_confirmation', booking_id=booking.booking_id)

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('checkout_process', screening_id=screening_id)

    total_cost = float(request.session.get('total_cost', 0.0))

    return render(request, 'booking/checkout_process.html', {
        'screening': screening,
        'movie': movie,
        'selected_seats': selected_seats,
        'adult_count': adult_count,
        'senior_count': senior_count,
        'child_count': child_count,
        'total_cost': total_cost,
        'adult_price': movie.price,
        'senior_price': senior_price,
        'child_price': child_price,
    })


import json
from django.http import JsonResponse

@login_required
def select_saved_card(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            card_id = data.get('card_id')

            if not card_id:
                return JsonResponse({'success': False, 'error': 'No card ID provided.'}, status=400)

            # Validate if the card belongs to the customer
            customer = request.user
            card = Card.objects.filter(id=card_id, customer=customer).first()
            if not card:
                return JsonResponse({'success': False, 'error': 'Invalid card selected.'}, status=400)

            # Store the card ID in session
            request.session['selected_card_id'] = card_id
            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def get_saved_cards(request):
    try:
        customer = request.user
        card_service = CardService()  # Initialize the CardService

        # Fetch customer cards using the service
        cards = card_service.get_customer_cards(customer)

        # Prepare card data for the response
        card_data = []
        for card in cards:
            try:
                decrypted_card_number = card_service.decrypt_card_number(card.card_number)
            except Exception as decrypt_error:
                # Log and skip cards that fail decryption
                print(f"Failed to decrypt card {card.id}: {decrypt_error}")
                continue

            card_data.append({
                'id': card.id,
                'decrypted_card_number': decrypted_card_number,
                'card_name': card.card_name,
            })

        return JsonResponse({'cards': card_data})

    except Exception as e:
        print(f"Error in get_saved_cards: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code', '').strip()
        total_cost = Decimal(request.session.get('total_cost', 0.0))

        # Case 1: No coupon code provided
        if not coupon_code:
            # Remove session data if no coupon is applied
            request.session.pop('promotion_id', None)
            request.session.pop('discount_amount', None)
            request.session.pop('new_total', None)
            return JsonResponse({
                'success': True,
                'message': 'No coupon applied.',
                'discount_amount': 0,
                'new_total': float(total_cost),
            })

        try:
            promotion = Promotion.objects.filter(promo_code__iexact=coupon_code).first()

            # Case 2: Invalid or expired coupon
            if not promotion:
                request.session.pop('promotion_id', None)
                request.session.pop('discount_amount', None)
                request.session.pop('new_total', None)
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid or expired coupon code.',
                })

            # Case 3: Check if the coupon has already been used by the customer
            if CouponUsage.objects.filter(customer=request.user, promotion=promotion).exists():
                request.session.pop('promotion_id', None)
                request.session.pop('discount_amount', None)
                request.session.pop('new_total', None)
                raise ValidationError("This coupon has already been used.")

            discount = Decimal(promotion.discount)
            discount_amount = (total_cost * discount) / Decimal(100)
            new_total = total_cost - discount_amount

            request.session['promotion_id'] = promotion.promo_code
            request.session['discount_amount'] = float(discount_amount)
            request.session['new_total'] = float(new_total)

            return JsonResponse({
                'success': True,
                'message': 'Coupon applied successfully!',
                'discount_amount': float(discount_amount),
                'new_total': float(new_total),
            })
        except ValidationError as ve:
            return JsonResponse({'success': False, 'error': str(ve)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})