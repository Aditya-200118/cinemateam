# accounts/services/user_service.py
from django.db import transaction
from accounts.repositories.user_repository import UserRepository
from accounts.repositories.address_repository import AddressRepository

class UserService:
    def __init__(self, user_repository=None, address_repository=None):
        self.user_repository = user_repository or UserRepository()
        self.address_repository = address_repository or AddressRepository()

    def register_customer(self, email, password, first_name, last_name, address_data, **extra_fields):

            if not address_data:
                raise ValueError("Address data is required to register a customer.")

            with transaction.atomic():
                address = self.address_repository.create_address(**address_data)

                customer = self.user_repository.create_customer(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    **extra_fields
                )
                customer.set_password(password)
                customer.save()

            return customer

    def create_address(self, billing_address, city, state, zip_code):
        return self.address_repository.create_address(billing_address, city, state, zip_code)

    def find_customer_by_email(self, email):
        return self.user_repository.get_customer_by_email(email)

    def update_customer_info(self, customer, **kwargs):
        return self.user_repository.update_customer(customer, **kwargs)

    def update_customer_address(self, address, **kwargs):
        return self.address_repository.update_address(address, **kwargs)
    
    def delete_customer(self, customer):

        return self.user_repository.delete_customer(customer)
    
    def find_customer_by_id(self, customer_id):
        return self.user_repository.get_customer_by_id(customer_id)
    
    def get_users_signed_up_for_promotions(self):

        return self.user_repository.get_users_signed_up_for_promotions()
