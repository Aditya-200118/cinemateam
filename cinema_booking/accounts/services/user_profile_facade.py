# accounts/services/user_profile_facade.py

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from accounts.services.user_service import UserService
import logging
from django.http import JsonResponse
from accounts.services.email_proxy import DjangoEmailService, EmailProxy

logger = logging.getLogger(__name__)

class UserProfileFacade:
    def __init__(self, user_service=None, email_service = None):
        """By default this will use the UserServices defined in accounts/services/user_service.py"""
        self.user_service = user_service or UserService()
        self.email_service = email_service or EmailProxy(DjangoEmailService())
    def create_customer(self, email, password, first_name, last_name, profile_data, address_data):

        if not address_data:
            raise ValueError("Address data is required to create a customer profile.")
        
        try:
            with transaction.atomic():
                # Delegate to UserService to handle both Customer and Address creation
                customer = self.user_service.register_customer(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    address_data=address_data,
                    **profile_data
                )
            return customer
        except Exception as e:
            logger.exception("Error creating customer profile: %s", str(e))
            raise e

    def update_user_profile(self, customer, profile_data, address_data):

        try:
            with transaction.atomic():
                # Update customer profile via UserService
                self.user_service.update_customer_info(customer, **profile_data)

                # Update the customer's address if it exists
                if customer.address:
                    self.user_service.update_customer_address(customer.address, **address_data)

                # Optional: Send email notification
                self.email_service.send_email(
                    subject="Profile Updated",
                    message="Your profile information has been updated.",
                    recipient_list=[customer.email],
                )
        except Exception as e:
            logger.exception("Error updating user profile: %s", str(e))
            raise e
    
    def delete_customer(self, request, customer_id):
        user_service = UserService()
        customer = user_service.find_customer_by_id(customer_id)
        
        if customer:
            success = user_service.delete_customer(customer)
            if success:
                return JsonResponse({'status': 'success', 'message': 'Customer deleted successfully.'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Customer deletion failed.'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Customer not found.'}, status=404)
