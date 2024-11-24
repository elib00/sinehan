from django.shortcuts import render, HttpResponse
from .models import Ticket
from movies.models import Movie
# Create your views here.


def purchaseTicket(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        
    except Movie.DoesNotExist:
        return HttpResponse("Movie not found")


         
