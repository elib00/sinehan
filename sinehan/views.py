from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from movies.models import Movie
from movies.views import movie_list
from django.db.models import Count
from django.core.serializers import serialize

def movies_view(request):
    return movie_list(request)

def home_view(request):
    movies = Movie.objects.all()
    movies_json = serialize('json', movies)
    
    return render(request, 'home.html', {'movies': movies, 'movies_json': movies_json})

def coming_view(request):
    unused_movies = Movie.objects.annotate(scheduled_count=Count('scheduled_movies')).filter(scheduled_count=0)
    
    return render(request, 'coming.html', {'unused_movies': unused_movies})