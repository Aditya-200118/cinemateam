from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Customer
from django import forms

class CustomerAdminForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set default values to False for non-superusers
        if not self.instance.is_superuser:
            self.fields['is_active'].initial = False
            self.fields['is_staff'].initial = False
            self.fields['is_superuser'].initial = False


class CustomerAdmin(BaseUserAdmin):
    form = CustomerAdminForm  # Use custom form
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Basic fields
        ('Personal info', {'fields': ('first_name', 'middle_name', 'last_name', 'contact_no')}),  # Personal information fields
        ('Address', {'fields': ('billing_address', 'city', 'state', 'zip_code')}),  # Address fields
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),  # Permissions fields
        ('Important dates', {'fields': ('last_login',)}),  # Important dates fields
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'middle_name', 'last_name',
                'contact_no', 'billing_address', 'city', 'state', 'zip_code',
                'password1', 'password2', 'is_staff', 'is_superuser', 'is_active',
            ),
        }),
    )

admin.site.register(Customer, CustomerAdmin)
