from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from movies.models import Movie
from movies.views import movie_list

def movies_view(request):
    return movie_list(request)

def home_view(request):
    return render(request, 'home.html')