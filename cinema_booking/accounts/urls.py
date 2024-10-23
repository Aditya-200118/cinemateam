from django.urls import path
from . import views
# from django.contrib.auth.views import LogoutView
from .views import CustomLogoutView 
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import CustomPasswordChangeView
from django.urls import path
from .views import activate_account

urlpatterns = [
    path("login/", views.user_login, name="user_login"),
    path("register/", views.register, name="register"),
    path("test_session/", views.test_session, name="test_session"),
    path("check_session/", views.check_session, name="check_session"),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),

]
#<a href="{% url 'logout' %}">Logout</a>
# path('register/step1/', views.register_step1, name='register_step1'),
# path('register/step2/', views.register_step2, name='register_step2'),
# path('register/step3/', views.register_step3, name='register_step3'),
