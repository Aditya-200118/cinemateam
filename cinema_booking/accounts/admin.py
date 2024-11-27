from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Customer, Address, Card
from admin.admin_views import admin_site

class CardInline(admin.TabularInline):
    model = Card
    extra = 1

class CustomerAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "middle_name", "last_name", "contact_no")},
        ),
        ("Address", {"fields": ("address",)}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "middle_name",
                    "last_name",
                    "contact_no",
                    "address",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )
    inlines = [CardInline]

class AddressAdmin(admin.ModelAdmin):
    list_display = ('billing_address', 'city', 'state', 'zip_code')
    search_fields = ('billing_address', 'city', 'state', 'zip_code')
    list_filter = ('city', 'state')

class CardAdmin(admin.ModelAdmin):
    list_display = ('customer', 'card_number', 'expiry_date', 'card_name')
    search_fields = ('customer__email', 'card_number')

# Register models with the custom admin site
admin_site.register(Customer, CustomerAdmin)
admin_site.register(Address, AddressAdmin)
admin_site.register(Card, CardAdmin)
