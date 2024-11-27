"""
URL configuration for cinema_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from admin.admin_views import admin_site, AdminLoginView, AdminLogoutView
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from accounts.views.customer_views import user_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/register', permanent=False)),
    path('admin/', admin_site.urls),
    path('accounts/', include('accounts.urls')),
    path('movie/', include('movie.urls')),
    path('booking/', include('booking.urls')), # Include booking app URLs
    path('admin/accounts/', admin_site.admin_view(admin_site.accounts_view), name='admin_accounts'),
    path('accounts/login/', user_login, name='user_login'),  # Custom user login view
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),  # Custom admin login view
    path('admin-logout/', AdminLogoutView.as_view(), name='admin_logout'),  # Custom admin logout view
    path('admin/welcome/', admin_site.admin_view(admin_site.welcome_view), name='admin_welcome'),
    path('admin/add-customer/', admin_site.admin_view(admin_site.add_customer_view), name='add_customer'), 
    path('admin/modify-customer/<int:pk>/', admin_site.admin_view(admin_site.modify_customer_view), name='modify_customer'),
    path('admin/customer-data/', admin_site.admin_view(admin_site.customer_data), name='customer_data'),
    path('admin/delete-customer/<int:pk>/', admin_site.admin_view(admin_site.delete_customer_view), name='delete_customer'),
    path('admin/movie/', admin_site.admin_view(admin_site.movie_admin_home), name='admin_movie'),
    path('admin/add-movie/', admin_site.admin_view(admin_site.add_movie), name='add_movie'),
    path('admin/movie-data', admin_site.admin_view(admin_site.movie_data_view), name='movie_data'),
    path('admin/showroom-schedule/<int:showroom_id>/', admin_site.admin_view(admin_site.showroom_schedule_view), name='showroom_schedule'),
    path('admin/manage_screenings/', admin_site.admin_view(admin_site.manage_screenings), name='manage_screenings'),
    path('admin/get_screenings/<int:movie_id>/<int:theatre_id>/<int:showroom_id>', admin_site.admin_view(admin_site.get_screenings), name='get_screenings'),
    path('admin/create_promotion/', admin_site.admin_view(admin_site.create_promotion), name="create_promotions")
]
"""This is only for development environment."""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('admin/movie/delete/<int:pk>/', admin_site.admin_view(movie_admin_views.delete_screening_view), name='delete_screening'),