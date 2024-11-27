from . import *

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['promo_code', 'title', 'description', 'discount', 'valid_from', 'valid_to']
class CouponForm(forms.Form):
    coupon_code = forms.CharField(max_length=50, required=True, label="Coupon Code")
