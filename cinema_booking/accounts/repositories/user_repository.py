# accounts/repositories/user_repository.py

from accounts.models import Customer, Card
from django.db import transaction
class UserRepository:
    
    @staticmethod
    def get_customer_by_email(email):
        return Customer.objects.filter(email=email).first()

    @staticmethod
    def create_customer(email, first_name, last_name, address, **kwargs):
        customer = Customer(
            email=email,
            first_name=first_name,
            last_name=last_name,
            address=address,
            **kwargs
        )
        customer.save()
        return customer

    @staticmethod
    def get_customer_by_id(customer_id):
        return Customer.objects.filter(user_id=customer_id).first()

    @staticmethod
    def update_customer(customer, **kwargs):
        for attr, value in kwargs.items():
            setattr(customer, attr, value)
        customer.save()
        return customer

    @staticmethod
    def delete_customer(customer):
        if customer:
            customer.delete()
            return True
        return False
    
    @staticmethod
    @transaction.atomic
    def delete_customer(customer):
        if customer:
            # Delete associated cards
            cards = Card.objects.filter(customer=customer)
            cards.delete()
            
            # Delete associated address
            if customer.address:
                customer.address.delete()
            
            # Finally, delete the customer
            customer.delete()
            return True
        return False

    @staticmethod
    def get_users_signed_up_for_promotions():
        return Customer.objects.filter(promotions=True)
