from django.urls import path
from movie.views.home_views import home, movie_details


urlpatterns = [
    path('home/', home, name='home'),
    path('movie/<int:movie_id>/', movie_details, name='movie_details'),
]
