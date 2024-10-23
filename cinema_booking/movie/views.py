from django.shortcuts import render

# Create your views here.
from .models import Movie
# Create your views here.
def home(request):
    search_query = request.GET.get('search', '')
    if search_query:
        movies = Movie.objects.filter(title__icontains=search_query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movie/home.html', {'movies': movies})


