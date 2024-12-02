from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from movies.models import Movie
from movies.views import movie_list
from django.db.models import Count
from django.core.serializers import serialize
from accounts.forms import CustomUserCreationForm

def movies_view(request):
    return movie_list(request)

def home_view(request):
    movies = Movie.objects.all()
    movies_json = serialize('json', movies)
    form = CustomUserCreationForm()
    
    return render(request, 'home.html', {'movies': movies, 'movies_json': movies_json, 'form': form})

def coming_view(request):
    form = CustomUserCreationForm()
    unused_movies = Movie.objects.annotate(scheduled_count=Count('scheduled_movies')).filter(scheduled_count=0)
    
    return render(request, 'coming.html', {'unused_movies': unused_movies, 'form': form})