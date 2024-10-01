from django.db import models
from accounts.models import CustomUser
from movies.models import Movie

class Cinema(models.Model):
    capacity = models.PositiveIntegerField(default=0)
    cinema_number = models.PositiveIntegerField()
    
class ScheduledMovie(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="cinema_scheduled_movies")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="scheduled_movies")
    audience_number = models.PositiveIntegerField(default=0)
    schedule = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_tickets")
    scheduled_movie = models.ForeignKey(ScheduledMovie, on_delete=models.CASCADE, related_name="movie_tickets")
    seat_identifier = models.CharField(max_length=3, default="")
    is_active = models.BooleanField(default=True)