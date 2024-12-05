from django.urls import path
from . import views
from accounts.views.password_views import *
from accounts.views.customer_views import CustomLogoutView, register, activate_account, check_email_exists
from accounts.views.profile_views import profile_view, edit_profile
from accounts.views.card_views import modify_payment_method, show_payment_methods, delete_payment_method
from accounts.views.order_history import order_history, get_tickets_for_booking

urlpatterns = [
    path("register/", register, name="register"),
    path("check-email/", check_email_exists, name="check_email_exists"),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('reset/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password_reset/done/', password_reset_done, name='password_reset_done'),
    path('reset/done/', password_reset_complete, name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('change_password/', change_password_view, name='change_password'),
    path('get-tickets/<int:booking_id>/', get_tickets_for_booking, name='get_tickets_for_booking'),
    path('logout/', CustomLogoutView.as_view(), name='user_logout'),
    path('profile/', profile_view, name='profile'),
    path("order-history/", order_history, name="order_history"),
    path('payment-methods/', show_payment_methods, name='show_payment_methods'),
    path('payment-methods/modify/<int:card_id>/', modify_payment_method, name='modify_payment_method'),
    path('payment-methods/modify/', modify_payment_method, name='modify_payment_method'),
    path('payment-methods/delete/<int:card_id>/', delete_payment_method, name='delete_payment_method'),
]