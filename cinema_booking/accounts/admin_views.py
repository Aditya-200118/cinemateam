# accounts/admin_views.py
from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from .models import Customer, Address, Card

class MyAdminSite(AdminSite):
    site_header = 'Cinema Booking Admin'
    site_title = 'Cinema Booking Admin Portal'
    index_title = 'Welcome to Cinema Booking Admin'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
            path('welcome/', self.admin_view(self.welcome_view), name='admin_welcome'),
            path('accounts/', self.admin_view(self.accounts_view), name='admin_accounts')
        ]
        return custom_urls + urls

    def welcome_view(self, request):
        context = {
            'num_movies': 10,  # Replace with actual query
            'num_users': 150,  # Replace with actual query
            'num_admins': 5,   # Replace with actual query
            'active_promos': 2,  # Replace with actual query
        }
        return render(request, 'admin/welcome.html', context)

    def accounts_view(self, request):
        return render(request, 'admin/accounts.html')

admin_site = MyAdminSite(name='myadmin')
