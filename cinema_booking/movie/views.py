from django.shortcuts import render

# Create your views here.
def home(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'movie/home.html')
