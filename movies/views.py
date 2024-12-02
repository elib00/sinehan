import json
from django.forms import model_to_dict
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Count
from accounts.models import CustomUser
from .models import Movie
from cinema.models import ScheduledMovie, Ticket


def movie_list(request):
    movies = Movie.objects.annotate(scheduled_count=Count('scheduled_movies')).filter(scheduled_count__gt=0)
    movies_json = serialize('json', movies)

    return render(request, 'movie_list.html', {'movies': movies, 'movies_json': movies_json})

def movie_details(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        return render(request, 'movie_details.html', {'movie': movie})
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found")
    
def movie_book(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        movie_data = model_to_dict(movie, fields=['id', 'movie_name', 'price'])
        scheduled_movies = ScheduledMovie.objects.filter(movie_id=movie_id, is_active=True)
        
        cinemas = {sm.cinema for sm in scheduled_movies}
        dates = {sm.schedule.date() for sm in scheduled_movies}
        times = {sm.schedule.time() for sm in scheduled_movies}
        
        
        valid_combinations = []
        for sm in scheduled_movies:
            valid_combinations.append({
                'id': sm.id,
                'cinema_name': sm.cinema.cinema_name,
                'date': sm.schedule.date().strftime('%b. %d, %Y'),
                'time': sm.schedule.time().strftime('%H:%M'),
                'seats': sm.seats
            })
        
        context = {
        'movie': json.dumps(movie_data),
        'valid_combinations': json.dumps(valid_combinations),
        'cinemas': cinemas,
        'dates': sorted(dates),  
        'times': sorted(time.strftime('%H:%M') for time in times),
        'actual_movie' : movie
        }

        return render(request, 'movie_book.html', context)
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found")
    

        
def movie_book_purchase(request, movie_id):
    if request.method == 'POST':
        user = request.user
        scheduled_movie_id = request.POST.get('scheduled_movie')
        seatsCodes = json.loads(request.POST.get('seats')) 
        
        try:
            scheduled_movie = ScheduledMovie.objects.get(id=scheduled_movie_id)
            
            
            tickets = [
                Ticket(user = user, scheduled_movie=scheduled_movie, seat_identifier=seat)
                for seat in seatsCodes
            ]
            
            Ticket.objects.bulk_create(tickets)
            scheduled_movie.update_seat_matrix()
            
            return render(request, 'home.html')
        except ScheduledMovie.DoesNotExist:
            return HttpResponse("Scheduled Movie not found", status=404)
    return HttpResponse("Invalid request method", status=405)