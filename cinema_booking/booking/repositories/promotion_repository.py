# booking/repository/promotion_repository.py

from booking.models import Promotion


class PromotionRepository:
    @staticmethod
    def create_promotion(promo_code, title, description, discount, valid_from, valid_to):
        return Promotion.objects.create(
            promo_code=promo_code,
            title=title,
            description=description,
            discount=discount,
            valid_from=valid_from,
            valid_to=valid_to
        )

    @staticmethod
    def get_promotion_by_code(promo_code):
        try:
            return Promotion.objects.filter(promo_code__iexact=promo_code).first()
        except Promotion.DoesNotExist:
            return None

    @staticmethod
    def filter_promotions(**kwargs):
        """Filter promotions based on given criteria."""
        return Promotion.objects.filter(**kwargs)

    @staticmethod
    def delete_promotion(promo_code):
        try:
            promotion = Promotion.objects.get(promo_code=promo_code)
            promotion.delete()
            return True
        except Promotion.DoesNotExist:
            return False
