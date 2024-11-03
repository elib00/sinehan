from django.db import models
from accounts.models import CustomUser
from movies.models import Movie

class Cinema(models.Model):
    capacity = models.PositiveIntegerField(default=0)
    cinema_name = models.CharField(max_length=100, default="")

class NowShowingMovie(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="cinema_showing_movies")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showing_movies")
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
class ScheduledMovie(models.Model):
    # cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name="cinema_scheduled_movies")
    # movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="scheduled_movies")
    audience_number = models.PositiveIntegerField(default=0)
    now_showing_movie = models.ForeignKey(NowShowingMovie, on_delete=models.CASCADE, related_name="now_showing_scheduled_movies")
    schedule = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_tickets")
    scheduled_movie = models.ForeignKey(ScheduledMovie, on_delete=models.CASCADE, related_name="movie_tickets")
    seat_identifier = models.CharField(max_length=3, default="")
    is_active = models.BooleanField(default=True)