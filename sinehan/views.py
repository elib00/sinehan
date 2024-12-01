from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from movies.models import Movie
from movies.views import movie_list
from django.core.serializers import serialize

def movies_view(request):
    return movie_list(request)

def home_view(request):
    movies = Movie.objects.all()
    movies_json = serialize('json', movies)
    
    return render(request, 'home.html', {'movies': movies, 'movies_json': movies_json})

def coming_view(request):
    return render(request, 'coming.html')