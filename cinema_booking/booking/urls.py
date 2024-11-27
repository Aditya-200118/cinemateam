from django.urls import path
from booking.views.booking_confirmation_view import booking_confirmation
from booking.views.seat_selection_view import seat_selection
from booking.views.select_showtime_view import select_showtime
from booking.views.checkout_process_view import checkout, apply_coupon, get_saved_cards, select_saved_card
urlpatterns = [
    path('showtime/<int:movie_id>/', select_showtime, name='select_showtime'),
    path('seat_selection/<int:screening_id>/', seat_selection, name='seat_selection'),
    path('confirmation/<int:booking_id>/', booking_confirmation, name='booking_confirmation'),
    path('checkout_process/<int:screening_id>/', checkout, name="checkout_process" ),
    path('apply-coupon/', apply_coupon, name='apply_coupon'),
    path('get-saved-cards/', get_saved_cards, name='get_saved_cards'),
    path('select-saved-cards/', select_saved_card, name='select_saved_cards'),
]

