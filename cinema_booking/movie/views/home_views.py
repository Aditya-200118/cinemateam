from . import *
from movie.services.movie_service import MovieService
from movie.models import Movie
from django.shortcuts import render, get_object_or_404

def home(request):
    today = timezone.now().date()
    search_query = request.GET.get('search', '')
    search_type = request.GET.get('search_type', 'title')
    release_date = request.GET.get('release_date', None)

    now_playing = None
    coming_soon = None

    if release_date:
        # Convert release_date string to a datetime object
        try:
            release_date = timezone.datetime.strptime(release_date, "%Y-%m-%d").date()
        except ValueError:
            release_date = None  # Ignore invalid date input

    if search_query:
        # Search with query and type
        if search_type == 'category':
            now_playing = MovieService.get_now_playing_by_category(search_query, release_date)
            coming_soon = MovieService.get_coming_soon_by_category(search_query, release_date)
        elif search_type == 'title':
            now_playing = MovieService.get_now_playing_by_title(search_query, release_date)
            coming_soon = MovieService.get_coming_soon_by_title(search_query, release_date)
    elif release_date:
        # Search only by release_date
        now_playing = MovieService.get_movies_by_release_date(release_date, now_playing=True)
        coming_soon = MovieService.get_movies_by_release_date(release_date, now_playing=False)
    else:
        # Default behavior
        now_playing = MovieService.get_now_playing_movies()
        coming_soon = MovieService.get_coming_soon_movies()

    return render(request, 'movie/home.html', {
        'now_playing': now_playing,
        'coming_soon': coming_soon,
        'search_query': search_query,
        'search_type': search_type,
        'selected_date': release_date,
    })



def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    
    return render(request, 'movie/movie_details.html', {'movie': movie})
