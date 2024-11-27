from . import models, ValidationError

class Address(models.Model):
    billing_address = models.CharField(max_length=255, default="")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    zip_code = models.CharField(max_length=10, default="")

    def clean(self):
        if self.pk and hasattr(self, "customer"):
            if self.customer and self.customer.pk != self.pk:
                raise ValidationError("A customer can only have one address.")