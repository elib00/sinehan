from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from movies.models import Movie

def movies_view(request):
    movies = Movie.objects.all()
    return render(request, 'movies.html', {'movies': movies})

def home_view(request):
    return render(request, 'home.html')