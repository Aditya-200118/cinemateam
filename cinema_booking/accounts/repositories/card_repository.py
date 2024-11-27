# accounts/repository/card_repository.py

from accounts.models import Card

class CardRepository:
    @staticmethod
    def create_card(customer, card_data):
        card = Card(customer=customer, **card_data)
        card.save()
        return card

    @staticmethod
    def get_cards_by_customer(customer):
        return customer.cards.all()

    @staticmethod
    def delete_card(card):
        card.delete()

    @staticmethod
    def update_card(card, updated_data):
        for field, value in updated_data.items():
            setattr(card, field, value)
        card.save()
        return card