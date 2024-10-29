from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Movie


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})

def movie_details(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        return render(request, 'movie_details.html', {'movie': movie})
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found")
    
def movie_book(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        return render(request, 'movie_book.html', {'movie': movie})
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found")