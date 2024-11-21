from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Movie
from cinema.models import ScheduledMovie


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
        scheduled_movies = ScheduledMovie.objects.filter(movie_id=movie_id, is_active=True)
        
        cinemas = {sm.cinema for sm in scheduled_movies}
        dates = {sm.schedule.date() for sm in scheduled_movies}
        
        context = {
        'movie': movie,
        'scheduled_movies': scheduled_movies,
        'cinemas': cinemas,
        'dates': sorted(dates),  
        }

        return render(request, 'movie_book.html', context)
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found")