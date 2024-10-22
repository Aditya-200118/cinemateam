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
from accounts.admin_views import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('accounts/', include('accounts.urls')),
    path('movie/', include('movie.urls')),
    path('admin/accounts/', admin_site.admin_view(admin_site.accounts_view), name='admin_accounts'),
]
