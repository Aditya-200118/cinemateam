from . import *
from movie.services.movie_service import MovieService
from movie.models import Movie
from django.shortcuts import render, get_object_or_404

# views.py
def home(request):
    today = timezone.now().date()
    search_query = request.GET.get('search', '')
    search_type = request.GET.get('search_type', 'title')  # Default to searching by title

    # Initialize variables for rendering
    now_playing = None
    coming_soon = None

    if search_query:
        # Search logic for now playing and coming soon based on search type
        if search_type == 'category':
            now_playing = MovieService.get_now_playing_by_category(search_query)
            coming_soon = MovieService.get_coming_soon_by_category(search_query)
        elif search_type == 'title':
            now_playing = MovieService.get_now_playing_by_title(search_query)
            coming_soon = MovieService.get_coming_soon_by_title(search_query)
    else:
        # Fetch all now playing and coming soon movies when no search query is present
        now_playing = MovieService.get_now_playing_movies()
        coming_soon = MovieService.get_coming_soon_movies()

    return render(request, 'movie/home.html', {
        'now_playing': now_playing,
        'coming_soon': coming_soon,
        'search_query': search_query,
        'search_type': search_type,
    })


def movie_details(request, movie_id):
    # Fetch the movie by ID, or return a 404 if not found
    movie = get_object_or_404(Movie, movie_id=movie_id)
    
    # Render the movie details page with the movie object
    return render(request, 'movie/movie_details.html', {'movie': movie})
