from django.urls import path
from .views import register, activate, user_login

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
