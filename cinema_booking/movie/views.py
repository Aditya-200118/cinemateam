from django.shortcuts import render

# Create your views here.
def movie(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'movie/home.html')