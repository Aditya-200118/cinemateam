# booking/services/promotion_service.py

from . import PromotionRepository, ValidationError
from booking.models.promotion_model import CouponUsage
from django.utils import timezone
from . import PromotionRepository, ValidationError
from django.utils import timezone

class PromotionService:
    @staticmethod
    def create_promotion(promo_code, title, description, discount, valid_from, valid_to):
        promotion = PromotionRepository.create_promotion(promo_code, title, description, discount, valid_from, valid_to)
        if not promotion:
            raise ValidationError("Failed to create promotion.")
        return promotion

    @staticmethod
    def get_promotion_by_code(promo_code):
        promotion = PromotionRepository.get_promotion_by_code(promo_code)
        if not promotion:
            raise ValidationError("Promotion not found.")
        return promotion

    @staticmethod
    def get_active_promotions():

        now = timezone.now()
        return PromotionRepository.filter_promotions(valid_from__lte=now, valid_to__gte=now)

    @staticmethod
    def delete_promotion(promo_code):
        if not PromotionRepository.delete_promotion(promo_code):
            raise ValidationError("Failed to delete promotion.")
        return True

    @staticmethod
    def get_future_promotions():

        now = timezone.now()
        return PromotionRepository.filter_promotions(valid_from__gt=now)

    @staticmethod
    def get_coupon(promo_code):

        promotion = PromotionRepository.get_promotion_by_code(promo_code)
        if not promotion:
            raise ValidationError("Coupon code is invalid.")

        # Ensure the promotion is active (within valid date range)
        now = timezone.now().date()
        if not (promotion.valid_from <= now <= promotion.valid_to):
            raise ValidationError("Coupon code is expired or not yet valid.")

        # Check that the discount is reasonable (e.g., not negative or too high)
        if promotion.discount < 0 or promotion.discount > 50:
            raise ValidationError("Coupon discount must be between 0% and 100%.")

        return promotion
    
    @staticmethod
    def validate_and_use_coupon(customer, promo_code):
        promotion = PromotionRepository.get_promotion_by_code(promo_code)
        print(f"The promotion is here (inside validate and use coupon): {promotion}")
        if not promotion:
            raise ValidationError("Coupon code is invalid.")

        # Ensure the promotion is active
        now = timezone.now().date()
        if not (promotion.valid_from <= now <= promotion.valid_to):
            raise ValidationError("Coupon code is expired or not yet valid.")

        # Check if the customer has already used the coupon
        if CouponUsage.objects.filter(customer=customer, promotion=promotion).exists():
            raise ValidationError("This coupon has already been used.")

        # Mark the coupon as used
        CouponUsage.objects.create(customer=customer, promotion=promotion)
        return promotion

    @staticmethod
    def promotion_exists_by_title(title):
        return PromotionRepository.filter_promotions(title__iexact=title).exists()

    @staticmethod
    def promotion_exists_by_title_or_code(title, promo_code):
        return (
            PromotionRepository.filter_promotions(title__iexact=title).exists() or
            PromotionRepository.filter_promotions(promo_code__iexact=promo_code).exists()
        )
