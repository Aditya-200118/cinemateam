# accounts/repositories/address_repository.py

from accounts.models import Address

class AddressRepository:
    @staticmethod
    def create_address(billing_address, city, state, zip_code):
        address = Address(
            billing_address=billing_address,
            city=city,
            state=state,
            zip_code=zip_code
        )
        address.save()
        return address

    @staticmethod
    def get_address_by_id(address_id):
        return Address.objects.filter(id=address_id).first()
    
    @staticmethod
    def update_address(address, **kwargs):
        for attr, value in kwargs.items():
            setattr(address, attr, value)
        address.save()
        return address

    @staticmethod
    def delete_address(address):
        address.delete()
